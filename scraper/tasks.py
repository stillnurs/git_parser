from celery import shared_task
import asyncio
import pandas as pd

from asyncio import Semaphore
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from .models import *

header = {'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
          'Chrome/86.0.4240.111 Safari/537.36'}
urls = Repository.objects.all()
sem = Semaphore(10)


@shared_task
# asynchronous function to fetch our urls from models.
async def fetch():
    async with ClientSession() as session:
        for url in urls:
            f'{url}/commits'
            async with session.get(url, headers=header) as response:
                html_body = await response.read()
        return {'body': html_body}


# same fetch() function but with Semaphore
"""
The value of these semaphores is that they allow us 
to protect resources from being overused.
"""


# and parsing data we need with bs4
@shared_task
async def fetch_with_sem():
    global sem
    async with sem:
        async with BeautifulSoup(fetch(), 'html.parser') as soup:
            content = soup.find_all('div', class_='TimelineItem--condensed')

            for data in content:
                title = ''.join(set(name.text for name in data.find_all(
                    'span', class_='commit-author ' 'user-mention')))

                message = data.p.find('a', class_='link-gray-dark').get_text()

                timestamp = data.find('h2').get_text()

            commitframe = pd.DataFrame({
                'title': title,
                'message': message,
                'timestamp': timestamp,
            })
            await Commits.objects.bulk_create(commitframe)
            print(commitframe)


# async function main creates asynchronous task
@shared_task
async def main():
    tasks = [asyncio.create_task(
        fetch()), await fetch_with_sem()]
    content = await asyncio.gather(*tasks)
    print(content)
    return content
