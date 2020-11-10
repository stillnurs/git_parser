import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'git_parser.settings')

app = Celery('git_parser')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get-list-urls': {
        'task': 'scraper.tasks.list_of_urls',
        'schedule': 10,
    },
    'run-main-task-scraper': {
        'task': 'scraper.tasks.task_scraper',
        'schedule': 12,
    },
    'run-task-save-data-to-db': {
        'task': 'scraper.tasks.save_to_db',
        'schedule': 14,
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
