
from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-tdn^p-3ecek17@nal9n!=vuvvvs&huca1175)!%gdkkl#4a(_0'

DEBUG = True

ALLOWED_HOSTS = ['moa-fh5j.onrender.com', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
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

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
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


# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'



TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"
LOGOUT_REDIRECT_URL = '/account/login/'
# LANGUAGES = [
#     ('en', 'English'),
#     ('ar', 'Arabic'),
#     # Add other languages you want to support
# ]





# JAZZMIN_SETTINGS = {
#     "custom_css": "your_app/css/jazzmin_rtl.css",
#     # other Jazzmin settings
# }


import os

# Set the path for the temporary PDF directory
TEMP_PDF_DIR = os.path.join(BASE_DIR, 'temp_pdfs')


LOGIN_URL='account/login/'



import logging
logger = logging.getLogger('weasyprint')
# Use the correct file path for the log file
log_file_path = os.path.join(TEMP_PDF_DIR, 'weasyprint.log')
logger.addHandler(logging.FileHandler(log_file_path))

import ssl

# Disable SSL certificate verification globally
ssl._create_default_https_context = ssl._create_unverified_context