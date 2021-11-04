from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# setting the Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_task.settings")
app = Celery("celery_task")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "debug": {
        "task": "assets.tasks.debug",
        "schedule": 1,
    },
}
app.conf.timezone = "UTC"
