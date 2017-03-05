"""
WSGI config for asana_task_analytics_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import socket

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asana_task_analytics_project.settings")

HOSTS = ['ubuntu']
if not socket.gethostname() in HOSTS:
    application = get_wsgi_application()
else:
    application = Cling(get_wsgi_application())


