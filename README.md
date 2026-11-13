# Smart Attendance Tracker System (Python Team Project)
### Phases 1, 2 & 3 Combined: Database Core, Visual Analytics & QR Automation

A complete, production-ready attendance tracking system built in Python. Designed for high academic marks, clean code presentation, and practical classroom utility.

---

## 🌟 Key Features

### Phase 1: Core Operations
- **Relational SQLite Database**: Structured schema with foreign keys, cascading deletes, and indexed query lookups.
- **Student Directory (CRUD)**: Add, edit, remove, search, and manage student profiles.
- **Session Attendance Recording**: Manual roll call with `Present`, `Absent`, and `Late` statuses.
- **Percentage Engine**:
  $$\text{Attendance \%} = \left(\frac{\text{Present} + 0.5 \times \text{Late}}{\text{Total Sessions}}\right) \times 100$$
- **Reports Export**: Generates styled `.xlsx` Excel sheets (with color-coded defaulter highlights) and standard `.csv` files.

### Phase 2: Role-Based Portals & Visual Analytics
- **Multi-Role Authentication**:
  - **Teacher / Admin Portal**: Full operational command over students, attendance sessions, live scanning, and analytics.
  - **Student Portal**: Restricted self-service view showing individual percentages, subject breakdowns, and digital ID card.
- **Interactive Visualizations**:
  - Class-wide attendance tier distribution (Excellent, Good, Warning, Critical).
  - Subject-by-subject average attendance bar charts.
  - Historical lecture attendance trend lines over time.
- **Automated Defaulter Warning System**:
  - Automatically flags anyone with attendance $< 75\%$.
  - Dispatches formal attendance shortage warning emails (built-in Mock Logging mode for zero-friction demonstration without requiring third-party credentials, plus optional live SMTP configuration).

### Phase 3: QR Code Automation & Multi-Interface
- **Printable Student ID Badges**: Generates professional graphic ID cards featuring student photo headers, details, and embedded QR codes.
- **Live Camera QR Scanner**: Turns any laptop webcam into a barcode/QR attendance scanner with audio beeps and instant database check-in.
- **Dual Interface Modes**:
  - **Modern Web Dashboard**: Runs on Flask (`app.py`).
  - **Terminal Menu (CLI)**: Interactive, formatted command-line runner (`cli.py`).

---

## 👥 Academic Team Member Work Breakdown

| Member | Assigned Role | Modules & Files Owned | Key Viva / Presentation Topics |
| :--- | :--- | :--- | :--- |
| **Member 1** | **Database & Data Layer** | `database/db.py`, `database/seed_data.py`, `services/student_service.py` | Schema design, Foreign Keys, SQL injection prevention, Student CRUD operations. |
| **Member 2** | **Attendance Engine & Reports** | `services/attendance_service.py`, `services/report_service.py`, `cli.py` | Attendance math formulas, Excel styling with `xlsxwriter`, CLI terminal workflow. |
| **Member 3** | **Frontend & UI/UX** | `templates/*.html`, `static/css/style.css`, `static/js/app.js` | Bootstrap 5 responsiveness, Jinja2 template inheritance, client-side table filters. |
| **Member 4** | **Automation, QR & Analytics** | `services/qr_service.py`, `services/analytics_service.py`, `services/email_service.py`, `static/js/qr_scanner.js` | QR matrix generation (`qrcode` + `Pillow`), HTML5 camera streaming, Chart.js, Email alerts. |

---

## 🚀 Quick Setup & Execution

### 1. Requirements
- Python 3.10+ (Fully compatible with Python 3.14)
- Install required packages:
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

### 3. Run the CLI Application (Terminal Mode)
```bash
python cli.py
```

---

## 🔑 Demo Test Credentials

The system comes pre-seeded with realistic sample data, subjects, and past attendance sessions:

| Account Type | Username / Roll No | Password | Description |
| :--- | :--- | :--- | :--- |
| **Teacher / Admin** | `admin` | `admin123` | Full administrative access to all tools. |
| **Teacher (Alternate)** | `prof_smith` | `teach123` | Course instructor account. |
| **Student (Eligible)** | `CS101` | `student123` | Rahul Sharma (Attendance: 100% - Good Standing). |
| **Student (Defaulter)** | `CS103` | `student123` | Amit Kumar (Attendance: ~33% - Debarment Warning Active). |
| **Student (Borderline)** | `CS107` | `student123` | Vikram Singh (Attendance: ~58% - Shortage Warning Active). |

---

## 📁 Project Structure

```text
attendance_tracker/
│
├── app.py                      # Flask web server & route handlers
├── cli.py                      # Interactive CLI terminal menu
├── config.py                   # Global configuration & thresholds (75%)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation & team division
│
├── database/
│   ├── __init__.py
│   ├── db.py                   # SQLite schema, tables & connection pool
│   └── seed_data.py            # Sample demo data loader
│
├── services/
│   ├── __init__.py
│   ├── student_service.py      # Student CRUD & course lookup logic
│   ├── attendance_service.py   # Attendance calculations, sessions & formulas
│   ├── qr_service.py           # QR badge graphics & payload encoders
│   ├── report_service.py       # Excel (.xlsx) & CSV export engines
│   ├── analytics_service.py    # Chart metrics, trends, and distribution tiers
│   └── email_service.py        # Warning notification dispatcher (Mock + SMTP)
│
├── static/
│   ├── css/
│   │   └── style.css           # Modern theme styling & status badges
│   └── js/
│       ├── app.js              # Table filtering, radio toggles & alerts
│       └── qr_scanner.js       # Live webcam QR scanner & audio feedback
│
└── templates/
    ├── base.html               # Shared layout & responsive navbar
    ├── login.html              # Multi-role login gateway with 1-click test buttons
    ├── teacher_dashboard.html  # KPI stats, recent lectures & action shortcuts
    ├── mark_attendance.html    # Session selector & manual roll-call sheet
    ├── qr_scanner.html         # Live webcam scanner & real-time scanned feed
    ├── students.html           # Student directory, modal editor & badge downloads
    ├── reports.html            # Defaulters list (<75%) & Excel/CSV download buttons
    ├── analytics.html          # Interactive Chart.js graphs & trend analysis
    ├── student_portal.html     # Student self-service dashboard & personal QR pass
    └── email_logs.html         # Sent shortage warning email dispatches
```
