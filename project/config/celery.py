from __future__ import absolute_import
import json
from django.conf import settings
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# TODO: set the settings to production or staging on the respective server
# TODO: currentlty it is set to the developer specific settings
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)




os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")

  # noqa

app = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
