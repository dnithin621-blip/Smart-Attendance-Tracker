import sys
import os
from datetime import datetime
from tabulate import tabulate

from database.db import init_db
from database.seed_data import seed
from services.student_service import (
    get_all_students, get_student_by_roll, add_student, get_all_courses, get_student_by_id
)
from services.attendance_service import (
    get_or_create_session, get_session_records, mark_batch_attendance,
    get_class_attendance_summary, get_student_overall_stats
)
from services.qr_service import generate_student_badge_card
from services.report_service import export_class_summary_csv, export_class_summary_excel
from services.email_service import alert_all_defaulters, send_defaulter_warning_email

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("=" * 65)
    print("   SMART ATTENDANCE TRACKER SYSTEM (CLI Edition)   ")
    print("   Phases 1, 2 & 3: Database, Analytics & QR Badges")
    print("=" * 65)

def list_students():
    print("\n--- ENROLLED STUDENTS DIRECTORY ---")
    students = get_all_students()
    if not students:
        print("No students found.")
        return
    table = [[s["roll_no"], s["full_name"], s["email"], s["department"], f"Sem {s['semester']}"] for s in students]
    print(tabulate(table, headers=["Roll No", "Name", "Email", "Department", "Semester"], tablefmt="grid"))

def handle_add_student():
    print("\n--- REGISTER NEW STUDENT ---")
    roll = input("Enter Roll Number (e.g. CS109): ").strip().upper()
    name = input("Enter Full Name: ").strip()
    email = input("Enter Email Address: ").strip()
    dept = input("Enter Department [Computer Science]: ").strip() or "Computer Science"
    sem = input("Enter Semester [4]: ").strip() or "4"

    try:
        sem = int(sem)
    except ValueError:
        sem = 1

    success, msg = add_student(roll, name, email, dept, sem)
    print(f"\n[Result]: {msg}")

def handle_mark_attendance():
    print("\n--- RECORD SESSION ATTENDANCE ---")
    courses = get_all_courses()
    for idx, c in enumerate(courses, 1):
        print(f"[{idx}] {c['course_code']} - {c['course_name']}")
    
    choice = input("\nSelect course number: ").strip()
    try:
        course = courses[int(choice) - 1]
    except Exception:
        print("Invalid course selection.")
        return

    today_str = datetime.now().date().isoformat()
    date_input = input(f"Enter Lecture Date [{today_str}]: ").strip() or today_str
    topic = input("Enter Lecture Topic [Regular Class]: ").strip() or "Regular Class"

    session_id = get_or_create_session(course["id"], date_input, topic, created_by="cli_admin")
    records = get_session_records(session_id)

    print(f"\nRecording attendance for {course['course_code']} ({date_input})")
    print("Options for each student: [P]resent (default), [A]bsent, [L]ate\n")

    batch = {}
    for r in records:
        status_input = input(f"{r['roll_no']} - {r['full_name']} (P/a/l) [{r['status']}]: ").strip().lower()
        if status_input == "a":
            batch[r["student_id"]] = "Absent"
        elif status_input == "l":
            batch[r["student_id"]] = "Late"
        else:
            batch[r["student_id"]] = "Present"

    success, msg = mark_batch_attendance(session_id, batch, marked_by="cli_admin")
    print(f"\n[Result]: {msg}")

def view_summary_and_defaulters():
    print("\n--- CLASS ATTENDANCE SUMMARY & DEFAULTER LIST (<75%) ---")
    summary = get_class_attendance_summary()
    if not summary:
        print("No attendance data recorded.")
        return

    table = []
    defaulter_count = 0
    for s in summary:
        status_label = "DEFAULTER" if s["is_defaulter"] else "Eligible"
        if s["is_defaulter"]:
            defaulter_count += 1
        table.append([
            s["roll_no"], s["full_name"], s["total_sessions"],
            s["present_count"], s["late_count"], s["absent_count"],
            f"{s['percentage']}%", status_label
        ])

    print(tabulate(table, headers=["Roll", "Name", "Total", "Pres", "Late", "Abs", "Pct %", "Status"], tablefmt="grid"))
    print(f"\nSummary: {len(summary)} total students | {defaulter_count} Defaulter(s) (<75% attendance).")

def check_individual_student():
    roll = input("\nEnter Student Roll Number to inspect (e.g. CS101): ").strip().upper()
    student = get_student_by_roll(roll)
    if not student:
        print("Student not found.")
        return

    stats = get_student_overall_stats(student["id"])
    print("\n" + "="*50)
    print(f" STUDENT: {student['full_name']} ({student['roll_no']})")
    print(f" Overall Attendance: {stats['overall_percentage']}%")
    print(f" Status: {'CRITICAL SHORTAGE (<75%)' if stats['is_defaulter'] else 'ELIGIBLE'}")
    print("="*50)

    breakdown_table = []
    for b in stats["breakdown"]:
        breakdown_table.append([
            b["course_code"], b["course_name"], b["total_sessions"],
            b["present_count"], b["late_count"], b["absent_count"], f"{b['percentage']}%"
        ])
    print(tabulate(breakdown_table, headers=["Code", "Course Name", "Total", "Pres", "Late", "Abs", "Pct %"], tablefmt="grid"))

def handle_generate_qr_badge():
    roll = input("\nEnter Student Roll Number to generate ID Badge (e.g. CS101): ").strip().upper()
    student = get_student_by_roll(roll)
    if not student:
        print("Student not found.")
        return

    badge_data = generate_student_badge_card(student)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{student['roll_no']}_badge.png")

    with open(out_file, "wb") as f:
        f.write(badge_data)

    print(f"\n[Success]: Generated high-res ID Card Badge with QR Code: {out_file}")

def handle_export_reports():
    print("\n--- EXPORT ATTENDANCE REPORTS ---")
    print("[1] Export to Excel (.xlsx)")
    print("[2] Export to CSV (.csv)")
    choice = input("Select format [1/2]: ").strip()

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(out_dir, exist_ok=True)

    if choice == "2":
        csv_data = export_class_summary_csv()
        out_path = os.path.join(out_dir, "attendance_summary.csv")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(csv_data)
        print(f"\n[Success]: CSV report exported to: {out_path}")
    else:
        excel_bytes = export_class_summary_excel()
        out_path = os.path.join(out_dir, "attendance_summary.xlsx")
        with open(out_path, "wb") as f:
            f.write(excel_bytes)
        print(f"\n[Success]: Styled Excel report exported to: {out_path}")

def handle_alert_defaulters():
    print("\n--- DISPATCH SHORTAGE ALERTS ---")
    summary = get_class_attendance_summary()
    defaulters = [s for s in summary if s["is_defaulter"]]
    if not defaulters:
        print("Great news! No students are currently below the 75% threshold.")
        return

    print(f"Found {len(defaulters)} student(s) below 75% attendance:")
    for d in defaulters:
        print(f" - {d['roll_no']}: {d['full_name']} ({d['percentage']}%) -> {d['email']}")

    confirm = input("\nSend warning emails to all defaulters? (y/N): ").strip().lower()
    if confirm == "y":
        count = alert_all_defaulters(defaulters)
        print(f"[Done]: Dispatched warning notifications to {count} students (Mock Mode logged).")

def main():
    init_db()
    while True:
        print_banner()
        print("  1. View All Registered Students")
        print("  2. Register New Student")
        print("  3. Record Daily Session Attendance (Roll Call)")
        print("  4. View Class Summary & Defaulter List (<75%)")
        print("  5. Check Individual Student Attendance Breakdown")
        print("  6. Generate Student QR ID Card Badge")
        print("  7. Export Reports to Excel / CSV")
        print("  8. Dispatch Low Attendance Warning Emails")
        print("  9. Seed / Reset Demo Database")
        print("  0. Exit CLI")
        print("-" * 65)

        choice = input("Enter your choice (0-9): ").strip()

        if choice == "1":
            list_students()
        elif choice == "2":
            handle_add_student()
        elif choice == "3":
            handle_mark_attendance()
        elif choice == "4":
            view_summary_and_defaulters()
        elif choice == "5":
            check_individual_student()
        elif choice == "6":
            handle_generate_qr_badge()
        elif choice == "7":
            handle_export_reports()
        elif choice == "8":
            handle_alert_defaulters()
        elif choice == "9":
            seed()
        elif choice == "0":
            print("\nExiting Smart Attendance Tracker. Goodbye!\n")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter 0-9.")

        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    main()
