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


BROKER_URL = 'redis://localhost:6379'  # TODO: on production, this has to be on RabbitMQ
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
