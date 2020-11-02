import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pandas import DataFrame

# from .models import Repository


url = 'https://github.com/stillnurs/myshop/commits/'

# url = Repository.objects.all()

limit = asyncio.Semaphore(10)


async def scraper():
    global limit
    async with limit:
        async with ClientSession() as session:
            async with session.get(url) as response:
                html_body = await response.read()
                soup = BeautifulSoup(html_body, 'html.parser')
                content = soup.find_all('div', class_='TimelineItem--condensed')
                commits = []
                for data in content:
                    message = data.p.find('a', class_='link-gray-dark').get_text()
                    commits.append({'message': message})

                    user = ''.join(set(name.text for name in data.find_all('span', class_='commit-author '
                                                                                          'user-mention')))
                    commits.append({'user': user})

                    timestamp = data.find('h2').get_text()
                    commits.append({'timestamp': timestamp})
                return commits


# committed_data = asyncio.run(scraper())
# print(committed_data)
