from __future__ import absolute_import, unicode_literals

from celery import shared_task

import time

from git_parser.scraper import ascrape


@shared_task
def scrape_commits():
    time.sleep(10)

    return time
