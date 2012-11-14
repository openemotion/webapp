import os

if os.getenv("MODE") == "production":
    DATABASE = "/home/dotcloud/current/data.db"
    SECRET_KEY = "8DC1DE50136CA4F4217E928893CA4866"
    DEBUG = True
else:
    DATABASE = "data.db"
    SECRET_KEY = "development key"
    DEBUG = True
    RECAPTCHA_PUBLIC_KEY = "6LeZF9kSAAAAAKrhqSW8ga1GLkez6_QdfyuKyrAQ"
    RECAPTCHA_PRIVATE_KEY = "6LeZF9kSAAAAAGYJW_jb-n8hS7tXMQEjbh5E9Jm7"
