import os

from celery import Celery

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
   'every-10-seconds': {
        'task': 'scraper.tasks.task_scraper',
        'schedule': 10,
    },
   'every-12-seconds': {
        'task': 'scraper.tasks.save_to_db',
        'schedule': 12,
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
