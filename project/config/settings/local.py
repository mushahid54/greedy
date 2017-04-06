from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DATABASE_NAME'),
        'USER': get_secret('DATABASE_USER'),
        'PASSWORD': get_secret('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',  # you can change this like: DATABASES['default']['PORT'] = 'some_other_port'
    }
}
