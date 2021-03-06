# configuration for production
import os
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
POSTMARK_API_KEY = os.environ['POSTMARK_API_KEY']
ENCRYPT_KEY = os.environ['OPENEM_ENCRYPT_KEY']
SECRET_KEY = os.environ['FLASK_SECRET_KEY']
ALWAYS_EMAIL = ["eli.finer@gmail.com", "yaelfiner@gmail.com"]
UPDATE_INTERVAL = 1000 * 60
DEBUG = False
