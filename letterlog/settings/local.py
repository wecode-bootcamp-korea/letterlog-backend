from .base    import *

DEBUG = True

ADMIN_ENABLED = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS.append('django_extensions')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

SHELL_PLUS = "ipython"
