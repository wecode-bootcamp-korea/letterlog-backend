import os

from .base    import *

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : os.environ.get('DJANGO_DB_NAME'),
        'USER'    : os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
        'HOST'    : os.environ.get('DJANGO_DB_HOST'),
        'PORT'    : os.environ.get('DJANGO_DB_PORT')
    }
}
