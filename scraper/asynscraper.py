import asyncio
from aiohttp import ClientSession
from asyncio import Semaphore
from bs4 import BeautifulSoup


from .models import Repository, Commits

# global variables to evade coroutine objects returned by async functions.
'''
Global variables were created in order to evade coroutine objects to be returned,
thus we can avoid bugs of native Django behavior while working with async functions,
while interacting with database models.
'''

commitframe = []
list_of_urls = []


# function get_url retrieves lists of url

def get_url():
    urls = [field for field in Repository.objects.values_list('url', flat=True)]
    for url in urls:
        list_of_urls.append(url)


# fetch function with Semaphore
"""
The value of these semaphores is that they allow us 
to protect resources from being overused.
"""
# and parsing data we need with bs4


async def fetch_with_sem(counter=0):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/86.0.4240.111 Safari/537.36'}

    sem = Semaphore(10)
    async with sem:
        async with ClientSession() as session:
            for url in list_of_urls:
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

                    counter += 1

                    df = {
                        'title': title,
                        'message': message,
                        'timestamp': timestamp,
                    }

                    commitframe.append(df)
                print(f'Total commits saved: {counter}')


# runner function for async web scraper
async def runner():
    tasks = asyncio.create_task(
        fetch_with_sem())
    await asyncio.gather(tasks)


# saving scraped data to database
def save_data():
    for dicts in commitframe:
        Commits.objects.bulk_create([Commits(
            title=dicts['title'],
            message=dicts['message'],
            timestamp=dicts['timestamp']
        )])

    print('About to save some data...')
