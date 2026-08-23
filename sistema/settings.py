"""Base settings for sistema project.

This file was extracted from the original single-file settings and kept mostly
unchanged apart from being organized as a base config. Use environment
variables for secrets and production overrides.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent


def load_env_file(path):
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        # In development prefer values from .env.local; overwrite existing env vars
        os.environ[key.strip()] = value.strip()


# Load local .env if present (development convenience)
load_env_file(BASE_DIR / '..' / '.env.local')


# SECURITY
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.getenv('DEBUG', 'True') in ('True', 'true', '1')
_raw_allowed = os.getenv('ALLOWED_HOSTS')
if not _raw_allowed or not _raw_allowed.strip():
    _raw_allowed = 'localhost,127.0.0.1,0.0.0.0,192.168.100.20,sistema'
ALLOWED_HOSTS = [h.strip() for h in _raw_allowed.split(',') if h.strip()]

# If DEBUG is False and ALLOWED_HOSTS is empty, provide a safe default
if not DEBUG and not ALLOWED_HOSTS:
    # In production you should set ALLOWED_HOSTS via env; default to localhost to avoid runserver errors
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Applications
INSTALLED_APPS = [
    'ordenes',
    'usuarios',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
    'ordenes.middleware.CurrentUserMiddleware',
]


ROOT_URLCONF = 'sistema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / '..' / 'templates', BASE_DIR / '..'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'sistema.wsgi.application'


# Database (default to sqlite for easier local setup)
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', str(BASE_DIR / '..' / 'db.sqlite3')),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'America/Denver')
USE_I18N = True
USE_TZ = True


# Static & media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '..' / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / '..' / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / '..' / 'media'


# Auth redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'


# Simple logging to console by default
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
}