import asyncio

from celery import shared_task
from .asyncraper import runner


@shared_task
def task_scraper():
    asyncio.run(runner())
