# -*- coding: utf-8 -*-
"""Dev settings."""
from .base import *
import os

DEBUG = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Set the email backend to a console backend since we cannot send email from
# this application
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
