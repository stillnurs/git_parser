import asyncio
from aiohttp import ClientSession
from asyncio import Semaphore
from bs4 import BeautifulSoup
import pandas as pd
from asgiref.sync import sync_to_async

from .models import Repository, Commits

# fetch function with Semaphore


"""
The value of these semaphores is that they allow us 
to protect resources from being overused.
"""

# and parsing data we need with bs4

commitframe = []


# title = []
# message = []
# timestamp = []


async def fetch_with_sem():
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/86.0.4240.111 Safari/537.36'}
    urls = ('https://github.com/realpython/Picha',)
    sem = Semaphore(10)
    async with sem:
        async with ClientSession() as session:
            for url in urls:
                url = f'{url}{"/commits"}'
                async with session.get(url, headers=header) as response:
                    html_body = await response.read()
                    soup = BeautifulSoup(html_body, 'html.parser')
                content = soup.find_all('div', class_='flex-auto min-width-0')

                for data in content:
                    title = (data.find('div', class_='f6 text-gray min-width-0').
                             find('a', class_='commit-author ''user-mention').get_text().strip('')
                             if data.find('a', class_='commit-author user-mention') else None)

                    message = (data.find('a', class_='link-gray-dark').get_text()
                               if data.find('a', class_='link-gray-dark') else None)

                    timestamp = (data.find('relative-time', class_='no-wrap').get_text()
                                 if data.find('relative-time', class_='no-wrap') else None)

                    df = {
                        'title': title,
                        'message': message,
                        'timestamp': timestamp,
                    }
                    print('---> First dict --->', df)

                    commitframe.append(df)
    print('---> Second dict --->', commitframe)


async def runner():
    tasks = asyncio.create_task(
        fetch_with_sem())
    await asyncio.gather(tasks)


def save_data():
    for dicts in commitframe:
        Commits.objects.bulk_create([Commits(
            title=dicts['title'],
            message=dicts['message'],
            timestamp=dicts['timestamp']
        )])

    print('About to save some data...')
