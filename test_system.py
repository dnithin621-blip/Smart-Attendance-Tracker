import sys
import os
import unittest

# Ensure project root in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_db, get_db_connection
from database.seed_data import seed
from services.student_service import get_all_students, get_student_by_roll, add_student
from services.attendance_service import get_class_attendance_summary, get_student_overall_stats, get_or_create_session
from services.qr_service import generate_student_badge_card, parse_qr_payload
from services.report_service import export_class_summary_csv, export_class_summary_excel
from services.analytics_service import get_dashboard_kpis
from services.email_service import send_defaulter_warning_email, get_email_logs
from app import app

class TestAttendanceTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        seed()

    def test_01_students_and_courses_exist(self):
        students = get_all_students()
        self.assertGreaterEqual(len(students), 8)
        s101 = get_student_by_roll("CS101")
        self.assertIsNotNone(s101)
        self.assertEqual(s101["full_name"], "Rahul Sharma")

    def test_02_attendance_calculations_and_defaulters(self):
        summary = get_class_attendance_summary()
        self.assertGreater(len(summary), 0)
        
        # Check that defaulters exist
        defaulters = [s for s in summary if s["is_defaulter"]]
        self.assertGreaterEqual(len(defaulters), 1, "At least one defaulter should be seeded for testing")
        
        # Verify CS103 is a defaulter (<75%)
        cs103 = next((s for s in summary if s["roll_no"] == "CS103"), None)
        self.assertIsNotNone(cs103)
        self.assertTrue(cs103["is_defaulter"])
        self.assertLess(cs103["percentage"], 75.0)

    def test_03_badge_generation(self):
        student = get_student_by_roll("CS101")
        badge_png = generate_student_badge_card(student)
        self.assertIsInstance(badge_png, bytes)
        self.assertTrue(badge_png.startswith(b"\x89PNG"), "Generated badge must be a valid PNG image")

    def test_04_reports_export(self):
        csv_str = export_class_summary_csv()
        self.assertIn("Roll No", csv_str)
        self.assertIn("CS101", csv_str)

        excel_bytes = export_class_summary_excel()
        self.assertIsInstance(excel_bytes, bytes)
        self.assertGreater(len(excel_bytes), 1000)

    def test_05_email_alert_dispatch(self):
        student = get_student_by_roll("CS103")
        success, msg = send_defaulter_warning_email(student, 33.3)
        self.assertTrue(success)
        logs = get_email_logs()
        self.assertGreater(len(logs), 0)
        self.assertEqual(logs[0]["roll_no"], "CS103")

    def test_06_flask_routes(self):
        client = app.test_client()

        # Login page
        res = client.get("/login")
        self.assertEqual(res.status_code, 200)

        # Login as teacher
        res = client.post("/login", data={"username": "admin", "password": "admin123"}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Teacher Dashboard", res.data)

        # View reports page
        res = client.get("/reports")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Attendance Reports", res.data)

        # View analytics page
        res = client.get("/analytics")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Visual Analytics", res.data)

        # Test API Scan endpoint
        session_id = get_or_create_session(course_id=1, session_date="2026-09-16", created_by="test")
        scan_res = client.post("/api/attendance/scan", json={"session_id": session_id, "qr_data": "CS101"})
        self.assertEqual(scan_res.status_code, 200)
        json_data = scan_res.get_json()
        self.assertTrue(json_data["success"])
        self.assertIn("Rahul Sharma", json_data["message"])

if __name__ == "__main__":
    unittest.main()
