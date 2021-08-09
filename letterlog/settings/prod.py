import os

from .base    import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

SECRET_ALGORITHM = os.environ.get('DJANGO_SECRET_ALGORITM')

# SECURITY WARNING: don't run with debug turned on in production!
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
