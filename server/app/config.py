SQLALCHEMY_DATABASE_URI = 'sqlite:///db/base.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'password'
SECURITY_PASSWORD_SALT = 'salt'
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
SECURITY_PASSWORD_HASH = 'bcrypt'
WTF_CSRF_ENABLED = False

CACHE_TYPE = "RedisCache"
CACHE_REDIS_URL = "redis://localhost:6379/0"
CACHE_DEFAULT_TIMEOUT = 300
DEBUG = False

# Upload Files Conf
UPLOAD_FOLDER = 'static/export/'
EMAIL_TEMPLATE = 'templates/'
PDF_FOLDER = 'static/pdf/'

# Celery
CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
