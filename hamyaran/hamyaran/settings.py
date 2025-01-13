from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# مسیرهای استاتیک و مدیا
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',  # پوشه‌ای که فایل‌های استاتیک در زمان توسعه در آن قرار دارند
]

STATIC_URL = '/static/'  # آدرس URL برای دسترسی به فایل‌های استاتیک
STATIC_ROOT = BASE_DIR / 'static'  # پوشه‌ای که فایل‌های استاتیک در هنگام اجرای collectstatic در آن جمع می‌شوند

MEDIA_URL = '/media/'  # آدرس URL برای دسترسی به فایل‌های مدیا
MEDIA_ROOT = BASE_DIR / 'media'  # مسیر ذخیره‌سازی فایل‌های مدیا

PWA_SERVICE_WORKER_PATH = BASE_DIR / 'staticfiles' / 'js' / 'service-worker.js'
PWA_SERVICE_WORKER_PATH = str(PWA_SERVICE_WORKER_PATH)  # تبدیل به رشته

LOGIN_REDIRECT_URL = "account:home"
LOGOUT_REDIRECT_URL = "services:home"
LOGIN_URL = "login"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '45.149.76.42']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'services.apps.ServicesConfig',
    'account.apps.AccountConfig',
    'django.contrib.humanize',
    'django_crontab',
    'extensions',
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap4',
    'dbbackup',
    'push_notifications',
    'django_jalali',
    'webpush',
    'django_gravatar',
    'pwa'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hamyaran.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hamyaran.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    }
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backups/'}

DBBACKUP_FILENAME_TEMPLATE = 'backup-{datetime}.dump'
DBBACKUP_MEDIA_FILENAME_TEMPLATE = 'media-backup-{datetime}.tar'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fa-IR'
TIME_ZONE = 'Asia/Tehran'
USE_TZ = True
USE_L10N = True
USE_I18N = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

AUTH_USER_MODEL = "account.User"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CRONJOBS = [
    ('0 * * * *', 'hamyaran.management.commands.generate_reminders')
]

PWA_APP_NAME = 'Hamyaran'
PWA_APP_DESCRIPTION = 'مدریت سلامت خانواده'
PWA_APP_THEME_COLOR = '#ffffff'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        "src": "/static/images/icons/icon-192x192.png",
        "sizes": "192x192"
    },
    {
        "src": "/static/images/icons/icon-512x512.png",
        "sizes": "512x512"
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/images/icons/icon-512x512.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'rtl'
PWA_APP_LANG = 'fa-IR'

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BIT7SPFOzYeu-B4_LPwi_0Q6maYZZAm4RdeX3-x7smauwCSmZC-iP1LnfwNQY5GwkDMRoFX7s4aA4cSLDYkyIHI",
    "VAPID_PRIVATE_KEY": "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JR0hBZ0VBTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEJHMHdhd0lCQVFRZ0kyZENzbG9CUG9XTFcrblUKWndFOStRSW1mbjJyY0ZWL2ZpeWwyVnoyMkhhaFJBTkNBQVNFKzBqeFRzMkhydmdlUHl6OEl2OUVPcG1tR1dRSgp1RVhYbDkvc2U3Sm1yc0FrcG1Rdm9qOVM1MzhEVUdPUnNKQXpFYUJWKzdPR2dPSEVpdzJKTWlCeQotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg",
    "VAPID_ADMIN_EMAIL": "acnobahar1@gmail.com",
}
