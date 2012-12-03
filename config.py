import os

if os.getenv("MODE") == "production":
    DATABASE = "/home/dotcloud/data/data.db"
    SECRET_KEY = "8DC1DE50136CA4F4217E928893CA4866"
    ENABLE_LONG_POLL = True
    UPDATE_INTERVAL = 5000
    DEBUG = True
else:
    DATABASE = "data.db"
    SECRET_KEY = "development key"
    ENABLE_LONG_POLL = True
    UPDATE_INTERVAL = 5000
    DEBUG = True
