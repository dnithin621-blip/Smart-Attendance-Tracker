import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    NAVY = RGBColor(30, 58, 138)
    DARK = RGBColor(15, 23, 42)
    GRAY = RGBColor(100, 116, 139)
    LIGHT_BG = RGBColor(241, 245, 249)
    WHITE = RGBColor(255, 255, 255)
    BLUE_ACCENT = RGBColor(37, 99, 235)
    GREEN = RGBColor(22, 163, 74)
    RED = RGBColor(220, 38, 38)

    blank_layout = prs.slide_layouts[6] # Blank slide

    def add_header(slide, title_text, category="SMART ATTENDANCE TRACKER"):
        # Top banner category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = BLUE_ACCENT

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = NAVY

    # =========================================================
    # SLIDE 1: Title Slide
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    # Background accent card
    bg_shape = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(11.733), Inches(5.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = NAVY
    bg_shape.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(10.9), Inches(4.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "SMART ATTENDANCE TRACKER"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Phases 1, 2 & 3 Combined: Database Core, Visual Analytics & QR Camera Automation"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(147, 197, 253)
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "\n• Python & SQLite3 Architecture  • Dynamic Student QR ID Badges  • Live Webcam Scanner\n• Role-Based Portals (Teacher vs Student)  • Interactive Chart.js Analytics  • Defaulter Alert Engine (<75%)"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.space_before = Pt(18)

    p4 = tf1.add_paragraph()
    p4.text = "\nPresented by: Python Project Team | Academic Session 2026"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = RGBColor(254, 240, 138)
    p4.space_before = Pt(20)

    # =========================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Industry Motivation")

    col_w = Inches(3.6)
    cards_data = [
        ("Traditional Manual Roll Call", [
            "Consumes 5 to 10 minutes per lecture hour.",
            "Prone to human entry errors and transcription mistakes.",
            "Wastes productive teaching time for university faculties."
        ], RED),
        ("Proxy & Identity Issues", [
            "Students easily sign or call out roll numbers for absent peers.",
            "Zero biometric or digital verification at the door.",
            "Leaves institution records vulnerable to manipulation."
        ], RED),
        ("Delayed Shortage Alerts", [
            "Attendance percentages calculated manually at the end of term.",
            "Students are unaware of shortages until debarred from exams.",
            "Lacks an automated warning mechanism for <75% attendance."
        ], RED)
    ]

    for idx, (head, points, color) in enumerate(cards_data):
        left_pos = Inches(0.8 + idx * 4.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.8), col_w, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), col_w - Inches(0.4), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(18)
        p_h.font.bold = True
        p_h.font.color.rgb = color

        for pt in points:
            p_b = tf.add_paragraph()
            p_b.text = "• " + pt
            p_b.font.size = Pt(13)
            p_b.font.color.rgb = DARK
            p_b.space_before = Pt(12)

    # =========================================================
    # SLIDE 3: Proposed Solution & Value Proposition
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Proposed Solution: The Smart Attendance Platform")

    sol_cards = [
        ("Instant QR Code Verification", [
            "Automated webcam roll call in under 1 second.",
            "Each student carries a unique digital QR ID badge.",
            "Built-in debouncing algorithm prevents duplicate scans."
        ], GREEN),
        ("Transparent Dual-Role Portals", [
            "Teacher Portal: Session marking, full roster, analytics & reports.",
            "Student Portal: Personal percentage, course standing & ID download.",
            "Eliminates miscommunication between teachers and students."
        ], BLUE_ACCENT),
        ("Continuous Analytics & Alerts", [
            "Live percentage calculations: (Present + 0.5*Late) / Total * 100.",
            "Instant flagging of students under 75% threshold.",
            "Automated warning dispatch system with complete audit logs."
        ], NAVY)
    ]

    for idx, (head, points, color) in enumerate(sol_cards):
        left_pos = Inches(0.8 + idx * 4.0)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.8), col_w, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), col_w - Inches(0.4), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(18)
        p_h.font.bold = True
        p_h.font.color.rgb = color

        for pt in points:
            p_b = tf.add_paragraph()
            p_b.text = "• " + pt
            p_b.font.size = Pt(13)
            p_b.font.color.rgb = DARK
            p_b.space_before = Pt(12)

    # =========================================================
    # SLIDE 4: System Architecture
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture & End-to-End Workflow")

    layers = [
        ("1. Presentation Layer (Dual Interface)", "Flask Web Application (Jinja2, Bootstrap 5, Chart.js) & Terminal CLI Runner (tabulate)", BLUE_ACCENT),
        ("2. Service & Business Logic Layer", "student_service | attendance_service | qr_service | report_service | analytics_service | email_service", NAVY),
        ("3. Hardware & Capture Layer", "Webcam Scanner (HTML5-QRCode) | Audio Feedback (Web Audio API) | Badge Graphics (Pillow)", BLUE_ACCENT),
        ("4. Data Persistence Layer", "SQLite 3 Relational Database (attendance.db) with 6 Normalized Tables & Foreign Key Constraints", NAVY)
    ]

    for idx, (l_title, l_desc, color) in enumerate(layers):
        top_pos = Inches(1.8 + idx * 1.25)
        bar = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(1.05))
        bar.fill.solid()
        bar.fill.fore_color.rgb = LIGHT_BG
        bar.line.color.rgb = color
        bar.line.width = Pt(2)

        tb = s4.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.1), Inches(11.3), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = l_title
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = color

        p_d = tf.add_paragraph()
        p_d.text = l_desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = DARK
        p_d.space_before = Pt(4)

    # =========================================================
    # SLIDE 5: Technology Stack
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Technology Stack & Engineering Decisions")

    tech_items = [
        ("Python 3.14", "Core Language", "Modern standard library, high performance, cross-platform portability."),
        ("SQLite 3", "Database", "Embedded, zero-configuration, ACID compliant, native Python support."),
        ("Flask 3.1", "Web Backend", "Lightweight micro-framework, decoupled routes, clean Jinja2 templating."),
        ("HTML5-QRCode", "Camera Scanner", "Client-side browser camera access with zero complex C-library dependencies."),
        ("Pillow & qrcode", "Graphics & Badges", "Renders high-res 360x480 student ID badges with embedded 2D QR matrix."),
        ("xlsxwriter", "Reporting", "Generates styled Excel reports with conditional formatting for defaulters."),
        ("Chart.js", "Visual Analytics", "Dynamic, responsive HTML5 canvas bar, line, and donut graphs."),
        ("tabulate", "CLI Formatter", "Grid-aligned terminal tables for command-line presentation mode.")
    ]

    for idx, (tech, role, why) in enumerate(tech_items):
        col = idx % 2
        row = idx // 2
        left_pos = Inches(0.8 + col * 6.0)
        top_pos = Inches(1.8 + row * 1.25)

        box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, top_pos, Inches(5.7), Inches(1.1))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_BG
        box.line.color.rgb = RGBColor(203, 213, 225)

        tb = s5.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.08), Inches(5.4), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{tech}  —  {role}"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = why
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK
        p2.space_before = Pt(3)

    # =========================================================
    # SLIDE 6: Database Architecture (SQLite Schema)
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Relational Database Design (SQLite)")

    tables_data = [
        ("users", "id, username, password_hash, role ('teacher'|'student'), full_name, email"),
        ("students", "id, roll_no (UNIQUE), full_name, email, department, semester"),
        ("courses", "id, course_code (UNIQUE), course_name, instructor, department"),
        ("attendance_sessions", "id, course_id (FK), session_date, session_topic, created_by, UNIQUE(course_id, session_date)"),
        ("attendance_records", "id, session_id (FK), student_id (FK), status ('Present'|'Absent'|'Late'), marked_at, UNIQUE(session_id, student_id)"),
        ("email_alerts", "id, student_id (FK), recipient_email, subject, message_body, sent_at, status")
    ]

    for idx, (tbl_name, cols) in enumerate(tables_data):
        top_pos = Inches(1.8 + idx * 0.85)
        bar = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(0.72))
        bar.fill.solid()
        bar.fill.fore_color.rgb = WHITE
        bar.line.color.rgb = BLUE_ACCENT
        bar.line.width = Pt(1)

        tb = s6.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.05), Inches(11.3), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"TABLE: {tbl_name.upper()}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = BLUE_ACCENT

        p_c = tf.add_paragraph()
        p_c.text = f"Columns: {cols}"
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = DARK

    # =========================================================
    # SLIDE 7: Phase 1 Deep Dive - Core Attendance Engine
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phase 1: Core Operations & Attendance Calculations")

    s7_box = s7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf7 = s7_box.text_frame
    tf7.word_wrap = True

    items7 = [
        ("Complete Student Directory (CRUD)", "Full ability to add, edit, delete, and list students with validation."),
        ("Session Scheduling", "Lectures linked to specific subjects and dates with lecture topic descriptions."),
        ("Interactive Roll-Call Sheet", "Manual marking table with 'Mark All Present' and 'Mark All Absent' quick-buttons."),
        ("Mathematical Attendance Formula", "Effective Attended = Present + (0.5 * Late)\nAttendance Percentage = (Effective Attended / Total Sessions) * 100"),
        ("Defaulter Identification", "Automatic threshold detection flagging students below 75.0%."),
        ("Multi-Format Reports", "Exports formatted Excel (.xlsx) with colored highlights and standard CSV files.")
    ]

    for idx, (title, desc) in enumerate(items7):
        p = tf7.paragraphs[0] if idx == 0 else tf7.add_paragraph()
        p.text = f"• {title}: "
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY
        if idx > 0:
            p.space_before = Pt(10)

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK

    # =========================================================
    # SLIDE 8: Phase 2 Deep Dive - Portals & Visual Analytics
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phase 2: Multi-Role Portals & Visual Analytics")

    p2_cards = [
        ("Teacher / Admin Portal", [
            "Full access to dashboard and roster.",
            "Session management & roll call.",
            "Live QR Scanner controls.",
            "Defaulter alert triggers & Excel export."
        ], NAVY),
        ("Student Self-Service Portal", [
            "Private login with roll number.",
            "Personal attendance % badge.",
            "Subject-by-subject attendance records.",
            "Download printable digital QR pass."
        ], BLUE_ACCENT),
        ("Interactive Visual Charts", [
            "Subject-wise Attendance Bar Chart.",
            "Attendance Tiers Donut Chart (>=90%, 75-89%, 60-74%, <60%).",
            "14-Day Attendance Trend Line Chart."
        ], GREEN)
    ]

    for idx, (head, points, color) in enumerate(p2_cards):
        left_pos = Inches(0.8 + idx * 4.0)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.8), col_w, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tb = s8.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.0), col_w - Inches(0.4), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(18)
        p_h.font.bold = True
        p_h.font.color.rgb = color

        for pt in points:
            p_b = tf.add_paragraph()
            p_b.text = "• " + pt
            p_b.font.size = Pt(13)
            p_b.font.color.rgb = DARK
            p_b.space_before = Pt(12)

    # =========================================================
    # SLIDE 9: Phase 3 Deep Dive - QR Badges & Live Camera Scanner
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phase 3: QR Code Badges & Live Camera Scanner")

    s9_box = s9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf9 = s9_box.text_frame
    tf9.word_wrap = True

    items9 = [
        ("Dynamic Student ID Badges", "Generates high-resolution graphical ID cards (360x480 PNG) with college header banner, photo placeholder, student details, and scannable 2D QR matrix using Pillow and qrcode."),
        ("Real-Time Webcam QR Scanner", "Uses HTML5-QRCode to stream live camera frames in the browser, detecting student QR badges in real time without any external software."),
        ("Instant Attendance API", "Async POST endpoint (/api/attendance/scan) verifies student identity and logs presence immediately without reloading the page."),
        ("Audio & Visual Confirmation", "Emits synthetic Web Audio API confirmation tones (high pitch for success, low pitch for errors) and renders real-time check-in stream."),
        ("Rapid-Scan Debouncing", "Built-in 3-second cooldown logic prevents accidental multiple scans of the same student badge."),
        ("Dual Interface (Web & CLI)", "Includes both the Flask Web Dashboard and an interactive Terminal CLI (cli.py).")
    ]

    for idx, (title, desc) in enumerate(items9):
        p = tf9.paragraphs[0] if idx == 0 else tf9.add_paragraph()
        p.text = f"• {title}: "
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY
        if idx > 0:
            p.space_before = Pt(10)

        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK

    # =========================================================
    # SLIDE 10: Automated Defaulter Alert Engine (<75%)
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Automated Defaulter Warning System (<75%)")

    box_alert = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.2))
    box_alert.fill.solid()
    box_alert.fill.fore_color.rgb = RGBColor(254, 242, 242)
    box_alert.line.color.rgb = RED
    box_alert.line.width = Pt(2)

    tb_a = s10.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(11.3), Inches(1.9))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True
    p_a1 = tf_a.paragraphs[0]
    p_a1.text = "CRITICAL SHORTAGE DETECTION & NOTIFICATION ENGINE"
    p_a1.font.size = Pt(18)
    p_a1.font.bold = True
    p_a1.font.color.rgb = RED

    p_a2 = tf_a.add_paragraph()
    p_a2.text = "• Real-Time Flagging: Flags any student falling below 75% attendance across all registered courses.\n• Single & Batch Alert Dispatches: Faculty can notify individual defaulters or click 'Alert All Defaulters'.\n• Built-in Mock Dispatcher: Logs all generated warnings into SQLite email_alerts table for seamless, offline viva presentation."
    p_a2.font.size = Pt(13)
    p_a2.font.color.rgb = DARK
    p_a2.space_before = Pt(8)

    box_sample = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.4))
    box_sample.fill.solid()
    box_sample.fill.fore_color.rgb = LIGHT_BG
    box_sample.line.color.rgb = RGBColor(203, 213, 225)

    tb_s = s10.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(11.3), Inches(2.1))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    p_s1 = tf_s.paragraphs[0]
    p_s1.text = "Sample Generated Warning Letter:"
    p_s1.font.size = Pt(14)
    p_s1.font.bold = True
    p_s1.font.color.rgb = NAVY

    p_s2 = tf_s.add_paragraph()
    p_s2.text = "\"Dear Amit Kumar (CS103), Your overall attendance has fallen to 33.3%, which is below the mandatory university cutoff of 75.0%. Please attend upcoming lectures to avoid exam debarment.\""
    p_s2.font.size = Pt(12)
    p_s2.font.italic = True
    p_s2.font.color.rgb = DARK
    p_s2.space_before = Pt(6)

    # =========================================================
    # SLIDE 11: Team Division of Work
    # =========================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Team Division of Work & Module Ownership")

    team_members = [
        ("Member 1", "Database & Data Layer", "database/db.py\ndatabase/seed_data.py\nservices/student_service.py", "Schema design, foreign keys, SQL injection defense, Student CRUD operations."),
        ("Member 2", "Attendance Engine & Reports", "services/attendance_service.py\nservices/report_service.py\ncli.py", "Attendance math formulas, Excel styling with xlsxwriter, Terminal CLI workflow."),
        ("Member 3", "Frontend & UI/UX", "templates/*.html\nstatic/css/style.css\nstatic/js/app.js", "Responsive Bootstrap 5 UI, Jinja2 template inheritance, client-side table filters."),
        ("Member 4", "Automation, QR & Analytics", "services/qr_service.py\nservices/analytics_service.py\nservices/email_service.py", "QR matrix generation, webcam scanning, Chart.js graphs, email alert logs.")
    ]

    for idx, (mem, role, files, topics) in enumerate(team_members):
        col_w_4 = Inches(2.8)
        left_pos = Inches(0.8 + idx * 3.0)

        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.8), col_w_4, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = BLUE_ACCENT
        card.line.width = Pt(1.5)

        tb = s11.shapes.add_textbox(left_pos + Inches(0.15), Inches(2.0), col_w_4 - Inches(0.3), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_m = tf.paragraphs[0]
        p_m.text = mem
        p_m.font.size = Pt(16)
        p_m.font.bold = True
        p_m.font.color.rgb = NAVY

        p_r = tf.add_paragraph()
        p_r.text = role
        p_r.font.size = Pt(12)
        p_r.font.bold = True
        p_r.font.color.rgb = BLUE_ACCENT
        p_r.space_before = Pt(4)

        p_f = tf.add_paragraph()
        p_f.text = f"\nFiles Owned:\n{files}"
        p_f.font.size = Pt(10)
        p_f.font.color.rgb = GRAY
        p_f.space_before = Pt(6)

        p_t = tf.add_paragraph()
        p_t.text = f"\nFocus Topics:\n{topics}"
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = DARK
        p_t.space_before = Pt(6)

    # =========================================================
    # SLIDE 12: Live Demonstration Workflow
    # =========================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Step-by-Step Live Demonstration Flow")

    demo_steps = [
        ("Step 1: Sign in as Teacher", "Login with admin / admin123 and highlight KPI cards and Defaulter warning banner."),
        ("Step 2: Live QR Scanner Demo", "Navigate to QR Scanner. Enter student CS101 or show badge to camera. Highlight instant audio beep and live feed."),
        ("Step 3: Student Directory & ID Cards", "Navigate to Students. Open student CS101 and showcase auto-generated printable ID Badge."),
        ("Step 4: Defaulter Review & Alert", "Open Reports. Highlight red defaulters (<75%). Click 'Send Warning to All Defaulters' and verify in Alert Logs."),
        ("Step 5: Student Portal Demonstration", "Logout and sign in as student CS103. Showcase personal critical shortage warning and subject breakdown."),
        ("Step 6: Terminal CLI Bonus", "Launch 'python cli.py' to show the examiner terminal-mode attendance calculations.")
    ]

    for idx, (title, desc) in enumerate(demo_steps):
        top_pos = Inches(1.8 + idx * 0.85)
        bar = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(11.733), Inches(0.72))
        bar.fill.solid()
        bar.fill.fore_color.rgb = LIGHT_BG
        bar.line.color.rgb = RGBColor(203, 213, 225)

        tb = s12.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.05), Inches(11.3), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p_c = tf.add_paragraph()
        p_c.text = desc
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = DARK

    # =========================================================
    # SLIDE 13: Future Scope & Enhancements
    # =========================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Future Scope & System Roadmap")

    future_items = [
        ("Biometric Face Recognition", "Incorporate OpenCV and deep learning face embeddings alongside QR codes for 2-factor authentication."),
        ("GPS Geofencing Check-in", "Allow students to check-in from their own phones only when physically inside lecture hall GPS coordinates."),
        ("SMS / WhatsApp Integration", "Connect with Twilio API to dispatch immediate WhatsApp/SMS alerts directly to guardians."),
        ("Hardware RFID / Scanner Integration", "Interface with USB barcode guns or physical RFID card readers via serial COM ports.")
    ]

    for idx, (f_title, f_desc) in enumerate(future_items):
        col = idx % 2
        row = idx // 2
        left_pos = Inches(0.8 + col * 6.0)
        top_pos = Inches(1.8 + row * 2.5)

        box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(5.7), Inches(2.2))
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_BG
        box.line.color.rgb = BLUE_ACCENT
        box.line.width = Pt(1.5)

        tb = s13.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.2), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f_title
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = f_desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK
        p2.space_before = Pt(8)

    # =========================================================
    # SLIDE 14: Conclusion & Q&A
    # =========================================================
    s14 = prs.slides.add_slide(blank_layout)
    bg_last = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(11.733), Inches(5.5))
    bg_last.fill.solid()
    bg_last.fill.fore_color.rgb = NAVY
    bg_last.line.fill.background()

    tb14 = s14.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(4.0))
    tf14 = tb14.text_frame
    tf14.word_wrap = True

    p_end1 = tf14.paragraphs[0]
    p_end1.text = "CONCLUSION & SUMMARY"
    p_end1.font.size = Pt(32)
    p_end1.font.bold = True
    p_end1.font.color.rgb = WHITE

    p_end2 = tf14.add_paragraph()
    p_end2.text = "• Successfully combined Phase 1 (Core & SQLite), Phase 2 (Portals & Analytics), and Phase 3 (QR & Webcam Scanning).\n• Replaces error-prone manual paper roll calls with an automated, tamper-resistant digital workflow.\n• Delivers transparent multi-user access for both instructors and students with proactive 75% shortage alerts.\n• Fully functional in both Web Dashboard (app.py) and Terminal CLI (cli.py) modes."
    p_end2.font.size = Pt(15)
    p_end2.font.color.rgb = RGBColor(226, 232, 240)
    p_end2.space_before = Pt(14)

    p_end3 = tf14.add_paragraph()
    p_end3.text = "\nThank You! Open for Questions & Evaluation."
    p_end3.font.size = Pt(22)
    p_end3.font.bold = True
    p_end3.font.color.rgb = RGBColor(254, 240, 138)
    p_end3.space_before = Pt(20)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "Attendance_Tracker_Presentation.pptx")
    prs.save(out_file)
    print(f"Presentation saved successfully to: {out_file}")

if __name__ == "__main__":
    create_deck()
