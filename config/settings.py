import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMPLATES_DIR = os.path.join(DATA_DIR, 'templates')
DATASETS_DIR = os.path.join(DATA_DIR, 'datasets')

# Create directories if they don't exist
for directory in [DATA_DIR, TEMPLATES_DIR, DATASETS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '',  # Add your Gmail
    'sender_password': ''  # Add your app password
}

# Fingerprint processing settings
FINGERPRINT_SETTINGS = {
    'template_file': os.path.join(TEMPLATES_DIR, 'templates.json'),
    'match_threshold': 0.7,  # Minimum similarity score for a match
    'max_features': 1000,  # Maximum number of features to extract
}

# OTP settings
OTP_SETTINGS = {
    'length': 6,
    'expiry_minutes': 5,
    'allowed_chars': '0123456789'
}

# GUI settings
GUI_SETTINGS = {
    'window_size': '800x600',
    'image_size': (300, 300),
    'font_family': 'Helvetica',
    'title_font_size': 14,
    'normal_font_size': 10
} 