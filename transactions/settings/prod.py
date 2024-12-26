from .base import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = False

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = False  # Proxy
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
USE_X_FORWARDED_HOST = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")

CORS_ORIGIN_WHITELIST = os.environ["DJANGO_CORS_ORIGIN_WHITELIST"].split(",")

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["POSTGRES_DB"],
        'HOST': os.environ["POSTGRES_HOST"],
        'POST': os.environ["POSTGRES_PORT"],
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': os.environ["POSTGRES_PASSWORD"],
    },
}
