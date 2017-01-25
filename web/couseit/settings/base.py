"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from .private_settings import (
    PHOST,
    PSECRET_KEY, PreCAPTCHA_SECRET_KEY,
    PEMAIL_HOST, PEMAIL_PORT, PEMAIL_HOST_USER, PEMAIL_HOST_PASSWORD,
    PEMAIL_USE_TLS, PEMAIL_USE_SSL
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# site url
HOST = PHOST

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = PSECRET_KEY

ALLOWED_HOSTS = ['*']

# EMAIL PART
EMAIL_HOST = PEMAIL_HOST
EMAIL_PORT = PEMAIL_PORT
EMAIL_HOST_USER = PEMAIL_HOST_USER
EMAIL_HOST_PASSWORD = PEMAIL_HOST_PASSWORD
EMAIL_USE_TLS = PEMAIL_USE_TLS
EMAIL_USE_SSL = PEMAIL_USE_SSL

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_gravatar',
    'rest_framework',
    'address',
    'account',
    'product',
    'stock'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'couseit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', os.path.join(BASE_DIR, 'templates')],
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


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend'
)

WSGI_APPLICATION = 'couseit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

HOST = PHOST

API_PATH = 'api/rest/v1'
API = '{0}/{1}'.format(HOST, API_PATH)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

PASSWORD_VALIDATION = 'django.contrib.auth.password_validation.'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': PASSWORD_VALIDATION + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': PASSWORD_VALIDATION + 'MinimumLengthValidator',
    },
    {
        'NAME': PASSWORD_VALIDATION + 'CommonPasswordValidator',
    },
    {
        'NAME': PASSWORD_VALIDATION + 'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Number format
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images, Media)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'www')
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# reCaptcha
reCAPTCHA_SITE_KEY = '6Ld9dA4UAAAAADMvh_ZnhfJp4P2hNUgE_fcSdDZt'
reCAPTCHA_SECRET_KEY = PreCAPTCHA_SECRET_KEY

# Authentication system
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/homepage'
LOGOUT_REDIRECT_URL = LOGIN_URL


# SESSION AGE 5 Minutes
TIME = 5 * 60
SESSION_COOKIE_AGE = TIME
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_IDLE_TIMEOUT = TIME