
DEBUG = True

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.mysql",
        # DB name or path to database file if using sqlite3.
        "NAME": "manai",
        # Not used with sqlite3.
        "USER": "root",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '###@gmail.com'
EMAIL_HOST_PASSWORD = '######'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = "######"
SERVER_EMAIL = "######"

#SANDBOX
PAYPAL_USER = "######"
PAYPAL_PASSWORD = "######"
PAYPAL_SIGNATURE = "######"

#CAMPAIGN MONITOR
CM_API_KEY = "######"
CM_CLIENT_ID = "######"
CM_RETAIL_LIST_ID = "######"
CM_WHOLESALE_LIST_ID = "######"
