import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asana_task_analytics_project.settings")
django.setup()

t0 = False
t1 = "2017-02-01T13:46:45.302Z"
t2 = "2017-02-27T19:09:14.226Z"

print(datetime.strptime(t1[:-5], '%Y-%m-%dT%H:%M:%S') < t0)
