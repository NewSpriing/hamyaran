from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hamyaran.settings')

app = Celery('hamyaran')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-reminders": {
        "task": "medicine.tasks.send_reminder_notifications",
        "schedule": crontab(minute="*"),  # هر دقیقه یک‌بار بررسی می‌کند
    },
}