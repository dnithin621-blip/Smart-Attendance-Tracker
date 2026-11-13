import os
import sys
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response, send_file
import io

from config import SECRET_KEY
from database.db import get_db_connection, init_db, hash_password
from database.seed_data import seed
from services.student_service import (
    get_all_students, get_student_by_id, get_student_by_roll,
    add_student, update_student, delete_student, get_all_courses, get_course_by_id
)
from services.attendance_service import (
    get_or_create_session, get_session_by_id, get_session_records,
    mark_single_attendance, mark_batch_attendance, get_student_overall_stats,
    get_class_attendance_summary, get_recent_sessions
)
from services.qr_service import (
    generate_qr_payload, parse_qr_payload, get_qr_image_base64, generate_student_badge_card
)
from services.report_service import (
    export_class_summary_csv, export_class_summary_excel
)
from services.analytics_service import (
    get_dashboard_kpis, get_course_analytics, get_attendance_distribution, get_daily_trend_data
)
from services.email_service import (
    send_defaulter_warning_email, alert_all_defaulters, get_email_logs
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# -------------------------------------------------------------
# Security & Access Control Decorators
# -------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        if session.get("role") not in ("teacher", "admin"):
            flash("Access restricted to teachers/administrators.", "danger")
            return redirect(url_for("student_portal"))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------
# Authentication Routes
# -------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, hash_password(password))
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]

            flash(f"Welcome back, {user['full_name']}!", "success")
            if user["role"] in ("teacher", "admin"):
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("student_portal"))
        else:
            flash("Invalid username/roll number or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("login"))

# -------------------------------------------------------------
# Teacher Portal & Dashboard
# -------------------------------------------------------------
@app.route("/")
@login_required
def root():
    if session.get("role") in ("teacher", "admin"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("student_portal"))

@app.route("/dashboard")
@teacher_required
def dashboard():
    kpis = get_dashboard_kpis()
    recent = get_recent_sessions(limit=6)
    return render_template("teacher_dashboard.html", kpis=kpis, recent_sessions=recent)

# -------------------------------------------------------------
# Student Management Routes
# -------------------------------------------------------------
@app.route("/students")
@teacher_required
def students_view():
    students = get_all_students()
    return render_template("students.html", students=students)

@app.route("/students/add", methods=["POST"])
@teacher_required
def add_student_route():
    roll_no = request.form.get("roll_no")
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    department = request.form.get("department", "Computer Science")
    semester = int(request.form.get("semester", 1))

    success, msg = add_student(roll_no, full_name, email, department, semester)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("students_view"))

@app.route("/students/edit/<int:student_id>", methods=["POST"])
@teacher_required
def edit_student_route(student_id):
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    department = request.form.get("department")
    semester = int(request.form.get("semester", 1))

    success, msg = update_student(student_id, full_name, email, department, semester)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("students_view"))

@app.route("/students/delete/<int:student_id>", methods=["POST"])
@teacher_required
def delete_student_route(student_id):
    success, msg = delete_student(student_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("students_view"))

@app.route("/students/<int:student_id>/badge")
@login_required
def download_student_badge(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student record not found.", "danger")
        return redirect(url_for("students_view"))

    # Only teacher or the student themselves can download badge
    if session.get("role") == "student" and session.get("username") != student["roll_no"]:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("student_portal"))

    badge_bytes = generate_student_badge_card(student)
    return send_file(
        io.BytesIO(badge_bytes),
        mimetype="image/png",
        as_attachment=False,
        download_name=f"{student['roll_no']}_badge.png"
    )

# -------------------------------------------------------------
# Attendance Marking (Manual & Batch)
# -------------------------------------------------------------
@app.route("/attendance/mark")
@teacher_required
def mark_attendance():
    courses = get_all_courses()
    course_id = request.args.get("course_id")
    session_date = request.args.get("session_date", datetime.now().date().isoformat())
    topic = request.args.get("topic", "")

    selected_course = None
    session_id = None
    records = []

    if course_id:
        course_id = int(course_id)
        selected_course = get_course_by_id(course_id)
        session_id = get_or_create_session(
            course_id=course_id,
            session_date=session_date,
            session_topic=topic or "Lecture Session",
            created_by=session.get("username", "admin")
        )
        records = get_session_records(session_id)

    return render_template(
        "mark_attendance.html",
        courses=courses,
        selected_course=selected_course,
        selected_date=session_date,
        selected_topic=topic,
        session_id=session_id,
        records=records
    )

@app.route("/attendance/save-batch", methods=["POST"])
@teacher_required
def save_attendance_batch():
    session_id = request.form.get("session_id")
    if not session_id:
        flash("Missing session identifier.", "danger")
        return redirect(url_for("mark_attendance"))

    records_dict = {}
    for key, value in request.form.items():
        if key.startswith("status_"):
            student_id = key.split("_")[1]
            records_dict[student_id] = value

    success, msg = mark_batch_attendance(session_id, records_dict, marked_by=session.get("username", "admin"))
    flash(msg, "success" if success else "danger")

    # Fetch session to redirect cleanly back to same session
    sess = get_session_by_id(session_id)
    if sess:
        return redirect(url_for("mark_attendance", course_id=sess["course_id"], session_date=sess["session_date"]))
    return redirect(url_for("mark_attendance"))

# -------------------------------------------------------------
# Phase 3: Live QR Code Scanner & Scanning API
# -------------------------------------------------------------
@app.route("/scanner")
@teacher_required
def qr_scanner_view():
    all_sessions = get_recent_sessions(limit=20)
    session_id = request.args.get("session_id")
    
    selected_session = None
    existing_records = []
    already_present_count = 0

    if session_id:
        selected_session = get_session_by_id(int(session_id))
    elif all_sessions:
        selected_session = all_sessions[0]

    if selected_session:
        existing_records = get_session_records(selected_session["id"])
        already_present_count = sum(1 for r in existing_records if r["status"] == "Present")

    return render_template(
        "qr_scanner.html",
        all_sessions=all_sessions,
        selected_session=selected_session,
        existing_records=existing_records,
        already_present_count=already_present_count
    )

@app.route("/api/attendance/scan", methods=["POST"])
@teacher_required
def api_scan_attendance():
    """API endpoint called asynchronously by client-side webcam QR scanner."""
    data = request.get_json() or {}
    session_id = data.get("session_id")
    qr_data = data.get("qr_data", "")

    if not session_id or not qr_data:
        return jsonify({"success": False, "message": "Missing session ID or QR code data."}), 400

    roll_no = parse_qr_payload(qr_data)
    student = get_student_by_roll(roll_no)

    if not student:
        return jsonify({"success": False, "message": f"Student with Roll '{roll_no}' not found."}), 404

    success, msg = mark_single_attendance(
        session_id=session_id,
        student_id=student["id"],
        status="Present",
        marked_by=session.get("username", "admin")
    )

    if success:
        return jsonify({
            "success": True,
            "message": f"Recorded: {student['full_name']} ({student['roll_no']})",
            "student": student
        })
    else:
        return jsonify({"success": False, "message": msg}), 500

# -------------------------------------------------------------
# Phase 2: Reports, Defaulter Tracking & Exports
# -------------------------------------------------------------
@app.route("/reports")
@teacher_required
def reports_view():
    courses = get_all_courses()
    course_id = request.args.get("course_id")
    summary = get_class_attendance_summary(int(course_id) if course_id else None)
    return render_template("reports.html", courses=courses, selected_course_id=course_id, summary=summary)

@app.route("/reports/export/excel")
@teacher_required
def export_excel_route():
    course_id = request.args.get("course_id")
    excel_bytes = export_class_summary_excel(int(course_id) if course_id else None)
    return send_file(
        io.BytesIO(excel_bytes),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="attendance_report.xlsx"
    )

@app.route("/reports/export/csv")
@teacher_required
def export_csv_route():
    course_id = request.args.get("course_id")
    csv_text = export_class_summary_csv(int(course_id) if course_id else None)
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance_report.csv"}
    )

# -------------------------------------------------------------
# Visual Analytics
# -------------------------------------------------------------
@app.route("/analytics")
@teacher_required
def analytics_view():
    course_stats = get_course_analytics()
    distribution = get_attendance_distribution()
    trend_data = get_daily_trend_data()
    return render_template(
        "analytics.html",
        course_stats=course_stats,
        distribution=distribution,
        trend_data=trend_data
    )

# -------------------------------------------------------------
# Email Shortage Alert System
# -------------------------------------------------------------
@app.route("/alerts/send/<int:student_id>", methods=["POST"])
@teacher_required
def send_single_alert_route(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash("Student record not found.", "danger")
        return redirect(url_for("reports_view"))

    stats = get_student_overall_stats(student_id)
    success, msg = send_defaulter_warning_email(student, stats["overall_percentage"])
    flash(msg, "info")
    return redirect(url_for("reports_view"))

@app.route("/alerts/send-all", methods=["POST"])
@teacher_required
def alert_all_defaulters_route():
    summary = get_class_attendance_summary()
    defaulters = [s for s in summary if s["is_defaulter"]]
    count = alert_all_defaulters(defaulters)
    flash(f"Warning notices successfully issued to {count} defaulter student(s).", "info")
    return redirect(url_for("reports_view"))

@app.route("/alerts/logs")
@teacher_required
def email_logs_view():
    logs = get_email_logs(limit=30)
    return render_template("email_logs.html", logs=logs)

# -------------------------------------------------------------
# Phase 2: Student Self-Service Portal
# -------------------------------------------------------------
@app.route("/portal")
@login_required
def student_portal():
    roll_no = session.get("username")
    student = get_student_by_roll(roll_no)
    
    # If a teacher views this page, allow them to view student CS101 as demo
    if not student and session.get("role") in ("teacher", "admin"):
        student = get_student_by_roll("CS101")

    if not student:
        flash("Student profile not found.", "warning")
        return redirect(url_for("login"))

    stats = get_student_overall_stats(student["id"])
    qr_payload = generate_qr_payload(student)
    qr_b64 = get_qr_image_base64(qr_payload)

    return render_template(
        "student_portal.html",
        student=student,
        stats=stats,
        qr_image_b64=qr_b64
    )

# -------------------------------------------------------------
# Main Entry Point
# -------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    # Seed automatically if database is fresh
    conn = get_db_connection()
    user_count = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
    conn.close()
    if user_count == 0:
        seed()

    print("\n" + "="*65)
    print(" 🚀 SMART ATTENDANCE TRACKER RUNNING (Phases 1, 2 & 3 Combined)")
    print("="*65)
    print(" Web Interface:    http://127.0.0.1:5000")
    print(" Teacher Login:    Username: 'admin'    | Password: 'admin123'")
    print(" Student Login:    Username: 'CS101'    | Password: 'student123'")
    print(" Defaulter Login:  Username: 'CS103'    | Password: 'student123'")
    print("="*65 + "\n")

    app.run(debug=True, host="127.0.0.1", port=5000)
