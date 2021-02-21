import asyncio

import httpx
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_text(url):
    try:
        r = requests.get(url, headers={'User-Agent': UserAgent().random})
        return r.text
    except Exception as e:
        print('ERROR: {}\r\n{}'.format(url, e))
        return None


async def get_text_async(url):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers={'User-Agent': UserAgent().random})
        return (r.text, None)
    except Exception as e:
        return (None, e)


async def get_html_async(url):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, headers={'User-Agent': UserAgent().random})
            html = BeautifulSoup(r.text, 'html.parser')
        return (html, None)
    except Exception as e:
        return (None, e)
