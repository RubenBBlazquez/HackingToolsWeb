import os
from celery import Celery

# if you want to launch celery worker, you must use the name HackingToolsWebCore
# for example celery -A HackingToolsWebCore worker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackingToolsWebCore.settings')

app = Celery('HackingToolsWeb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
