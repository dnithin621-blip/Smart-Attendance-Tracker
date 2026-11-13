import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'attendance.db')
EXPORTS_DIR = os.path.join(BASE_DIR, 'exports')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

# Application Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'antigravity-attendance-secret-key-2026')
ATTENDANCE_THRESHOLD_PERCENT = 75.0  # Standard college attendance requirement

# Email Notification Settings (Mock mode enabled for safe local testing and presentation)
MOCK_EMAIL_MODE = True
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'attendance-alert@college.edu')
