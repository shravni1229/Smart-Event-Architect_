import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_event_architect_secret_key_2026_bca_mini')
    DATABASE = os.path.join(BASE_DIR, 'event_architect.db')
    
    # Default Admin Credentials
    ADMIN_DEFAULT_NAME = 'Administrator'
    ADMIN_DEFAULT_EMAIL = 'admin@eventarchitect.com'
    ADMIN_DEFAULT_PASSWORD = 'admin123'
    
    # Currency
    CURRENCY_SYMBOL = '₹'
    
    # Allowed Event Types
    EVENT_TYPES = [
        'Wedding Ceremony & Reception',
        'Birthday Celebration',
        'Corporate Conference & Seminar',
        'College Cultural Fest',
        'Engagement Ceremony',
        'Anniversary Gala',
        'Farewell Party'
    ]
    
    # Request Status Options
    STATUS_OPTIONS = [
        'Pending',
        'In Review',
        'Plan Created',
        'Confirmed',
        'Completed',
        'Cancelled'
    ]
