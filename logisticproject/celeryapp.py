import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logisticproject.settings')

app = Celery('logisticproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
