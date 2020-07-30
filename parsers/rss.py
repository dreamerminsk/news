import asyncio
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta

from bs4 import BeautifulSoup


async def parse(text):
    soup = BeautifulSoup(text, 'xml')
    channel = {}
    for channel_node in soup.find_all('channel'):
        channel = await parse_channel(channel_node)
    return channel


async def parse_channel(node):
    channel = {}
    channel['title'] = node.find('title').text
    channel['link'] = node.find('link').text
    channel['description'] = node.find('description').text
    channel['items'] = []
    for item_node in node.find_all('item'):
        channel['items'].append(await parse_item(item_node))
    return channel


async def parse_item(item):
    article = {}
    article['title'] = item.find('title').text
    article['link'] = item.find('link').text
    if '?' in article['link']:
        article['link'] = article['link'][:article['link'].find('?')]
    article['last_access'] = datetime.now()
    return article
