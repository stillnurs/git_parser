import asyncio
import pandas as pd

from asyncio import Semaphore
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from ...models import *


class Scraper:
    def __init__(self):
        self.header = {'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/86.0.4240.111 Safari/537.36'}
        self.urls = Repository.objects.all()
        self.sem = Semaphore(10)

    async def fetch(self):
        async with ClientSession() as session:
            for url in self.urls:
                f'{url}/commits'
                async with session.get(url, headers=self.header) as response:
                    html_body = await response.read()
            return {'body': html_body}

    async def fetch_with_sem(self):
        async with self.sem:
            async with BeautifulSoup(self.fetch(), 'html.parser') as soup:
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

    async def main(self):
        tasks = [asyncio.create_task(
            self.fetch_with_sem())]
        content = await asyncio.gather(*tasks)
        return content

    def runner(self):
        results = asyncio.run(self.main())
        return results