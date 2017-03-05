from asana_task_analytics_project.secrets.secrets import *

# Heroku Deploy
import dj_database_url

DATABASES = dict()
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_ROOT = 'staticfiles'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
