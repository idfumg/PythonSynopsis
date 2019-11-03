import requests
from time import time

def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r

def write_file(response):
    filename = response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)

def main():
    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file(url))

#t0 = time()
#main()
#print(time() - t0)

import asyncio
import aiohttp

def write_image(data):
    filename = 'file-{}.jpeg'.format((int(time() * 1000)))
    with open(filename, 'wb') as file:
        file.write(data)

async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)

async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)

t0 = time()
asyncio.run(main2())
print(time() - t0)
