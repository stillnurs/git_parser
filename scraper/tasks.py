import asyncio
from datetime import time
import time

from celery import shared_task
from .asynscraper import runner, save_data, get_url


@shared_task
def list_of_urls():
    return get_url()


@shared_task
def task_scraper():
    asyncio.run(runner())


@shared_task
def save_to_db():
    print('Task, save_to_db is working now...')
    return save_data()
