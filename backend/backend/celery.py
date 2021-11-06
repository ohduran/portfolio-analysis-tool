from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# setting the Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_task.settings")
app = Celery("celery_task")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "debug": {
        "task": "assets.tasks.get_yesterday_stocks_equities_daily_open_close",
        "schedule": crontab(day_of_week="tue-sat", hour=3),
    },
}
app.conf.timezone = "UTC"
