import asyncio

from django.conf import settings

from aiohttp import ClientSession
from asyncio import Semaphore
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

from .models import Repository


# fetch function with Semaphore
"""
The value of these semaphores is that they allow us 
to protect resources from being overused.
"""


# and parsing data we need with bs4

async def fetch_with_sem():
    title = []
    message = []
    timestamp = []
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/86.0.4240.111 Safari/537.36'}
    urls = ('https://github.com/stillnurs/myshop', 'https://github.com/realpython/Picha')
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
                    title.append(data.find('div', class_='f6 text-gray min-width-0').
                                 find('a', class_='commit-author ''user-mention').get_text().strip('')
                                 if data.find('a', class_='commit-author user-mention') else None)

                    message.append(data.find('a', class_='link-gray-dark').get_text()
                                   if data.find('a', class_='link-gray-dark') else None)

                    timestamp.append(data.find('relative-time', class_='no-wrap').get_text()
                                     if data.find('relative-time', class_='no-wrap') else None)

        commitframe = pd.DataFrame({
            'title': title,
            'message': message,
            'timestamp': timestamp,
        })
        print(commitframe)

# save Dataframe data to DataBase
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        database_name = settings.DATABASES['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )

        engine = create_engine(database_url, echo=False)
        commitframe.to_sql('Commits', con=engine, if_exists='append', index=True)


async def runner():
    tasks = asyncio.create_task(
        fetch_with_sem())
    await asyncio.gather(tasks)


