
from pathlib import Path
import os
import dj_database_url
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'b7(55vlmh)#_h_k+-t)w9mpdn%tp^jo60$-m)d@7$lf7mnhgf5'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','https://moa-fh5j.onrender.com/','moa-fh5j.onrender.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'lov',
    'laboratory',
    'sample',
    'account',
    'tailwind',
    'theme',
    'widget_tweaks',
    'xhtml2pdf',
    'corsheaders',
    'fontawesomefree'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'core.urls'
CORS_ALLOW_ALL_ORIGINS = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES["default"] = dj_database_url.parse("postgresql://stagingmoadb_user:KJvzhTdkgpYoZws1S1J5BXRbpI506bb5@dpg-crtcom68ii6s73ekohqg-a.oregon-postgres.render.com/stagingmoadb")

# DATABASES = {
#     'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
# }


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




# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ar' 

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# STORAGES = {
#     # ...
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
# LANGUAGES = [
#     ('en', 'English'),
#     ('ar', 'Arabic'),
#     # Add other languages you want to support
# ]




# Set the path for the temporary PDF directory
TEMP_PDF_DIR = os.path.join(BASE_DIR, 'temp_pdfs')



LOGOUT_REDIRECT_URL = '/account/login/'
LOGIN_URL='account/login/'



logger = logging.getLogger('weasyprint')
# Use the correct file path for the log file
log_file_path = os.path.join(TEMP_PDF_DIR, 'weasyprint.log')
logger.addHandler(logging.FileHandler(log_file_path))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# import ssl
#
# # Disable SSL certificate verification globally
# ssl._create_default_https_context = ssl._create_unverified_context
#
#
# SECURE_HSTS_SECONDS = 3600  # Adjust the duration (in seconds) as needed
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Optional
# SECURE_HSTS_PRELOAD = True  # Optional
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

if os.getenv('DJANGO_PRODUCTION') == 'False':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False  # Disable for local development
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


import ssl

# Disable SSL certificate verification globally
ssl._create_default_https_context = ssl._create_unverified_context


# PDF Generation Settings
PDF_GENERATION = {
    'MAX_FILE_SIZE': 10 * 1024 * 1024,  # 10MB
    'ALLOWED_FONTS': ['Cairo-VariableFont_slnt,wght.ttf.ttf'],
    'ALLOWED_IMAGES': ['cert-logo.png', 'iqas2.png'],
}

# Ensure proper static file handling
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]