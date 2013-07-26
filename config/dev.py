# configuration for development
import os
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
SECRET_KEY = "secret"
ENCRYPT_KEY = "secret"
ALWAYS_EMAIL = ["eli.finer@gmail.com", "yaelfiner@gmail.com"]
UPDATE_INTERVAL = 5000
LOGFILE = None
DEBUG = True
