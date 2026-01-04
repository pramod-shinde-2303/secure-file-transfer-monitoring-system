import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Monitoring Configuration
MONITOR_PATH = os.path.join(DATA_DIR, 'monitoring_zone')
os.makedirs(MONITOR_PATH, exist_ok=True)

# Sensitive Classification
SENSITIVE_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.key', '.pem', '.sqlite']
SENSITIVE_KEYWORDS = ['confidential', 'secret', 'password', 'budget', 'salary']

# Policy Configuration
# Simulate an internal secure zone and an external "unauthorized" zone
SECURE_ZONE = os.path.join(MONITOR_PATH, 'secure_docs')
EXTERNAL_DEVICE_PATH = os.path.join(MONITOR_PATH, 'external_usb')

# Ensure these exist for the purpose of the demo
os.makedirs(SECURE_ZONE, exist_ok=True)
os.makedirs(EXTERNAL_DEVICE_PATH, exist_ok=True)

AUTHORIZED_PATHS = [SECURE_ZONE]
UNAUTHORIZED_PATHS = [EXTERNAL_DEVICE_PATH]

# Logging
LOG_FILE = os.path.join(LOG_DIR, 'audit.log')
