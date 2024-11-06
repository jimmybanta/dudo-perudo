"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.django['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# application definition 

ASGI_APPLICATION = 'backend.asgi.application'
WSGI_APPLICATION = 'backend.wsgi.application'


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_eventstream',
    'corsheaders',
    'rest_framework',
    'games'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.database['name'],
        'USER': config.database['user'],
        'PASSWORD': config.database['password'],
        'HOST': config.database['endpoint'], 
        'PORT': config.database['port'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/dudoperudo/static'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
CSRF_TRUSTED_ORIGINS = ['https://*.dudoperudo.com']

# configure allowed hosts and origins
if config.ENV == 'DEV':
    ALLOWED_HOSTS = ['*']

    CORS_ALLOWED_ORIGINS = ['http://localhost:3000']

elif config.ENV == 'STAG':
    ALLOWED_HOSTS = ['api-stag.dudoperudo.com', 'www.api-stag.dudoperudo.com',
                '127.0.0.1', 'localhost']
    
    CORS_ALLOWED_ORIGINS = ['https://*.dudoperudo.com', 'https://staging.dudoperudo.com']
    
elif config.ENV == 'PROD':
    ALLOWED_HOSTS = ['api.dudoperudo.com', 'www.api.dudoperudo.com']

    CORS_ALLOWED_ORIGINS = ['https://*.dudoperudo.com', 'https://dudoperudo.com']

# configure logging
if config.ENV == 'DEV':

    LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
} 

elif config.ENV == 'STAG' or config.ENV == 'PROD':

    # configure https
    ## set period to 6 days
    SECURE_HSTS_SECONDS = 518400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # configure logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                "format": (
                    u"%(asctime)s [%(levelname)-8s] "
                    "(%(module)s.%(funcName)s) %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",

            },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': '/var/log/django/django.log',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }