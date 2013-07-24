# configuration for production
import os
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
POSTMARK_API_KEY = os.environ['POSTMARK_API_KEY']
SECRET_KEY = os.environ['FLASK_SECRET_KEY']
UPDATE_INTERVAL = 5000
DEBUG = False
