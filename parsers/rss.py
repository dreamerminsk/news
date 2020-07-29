from datetime import datetime, timedelta
import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
import asyncio


async def parse(text):
    soup = BeautifulSoup(text, 'xml')
    for channel in soup.findall('channel'):
        for item in channel.findall('item'):
            article = await parse_item(item)


async def parse_item(item):
    item  = {}
    item.title = item.find('title').text
    item.link = item.find('link').text
    if '?' in link:
        link = link[:link.find('?')]
    feeds.update_one({'_id': feed['_id']}, {
                     '$set': {'last_access': datetime.now()}}, upsert=False)
    if i > 0:
        feeds.update_one({'_id': feed['_id']}, {
            '$set': {'ttl': 0.9 * feed['ttl']}}, upsert=False)
        feeds.update_one({'_id': feed['_id']}, {
            '$set': {'next_access': datetime.now() + timedelta(seconds=0.9 * feed['ttl'])
                     }}, upsert=False)
    else:
        feeds.update_one({'_id': feed['_id']}, {
            '$set': {'ttl': 1.1 * feed['ttl']}}, upsert=False)
        feeds.update_one({'_id': feed['_id']}, {
            '$set': {'next_access': datetime.now() + timedelta(seconds=1.1 * feed['ttl'])
                     }}, upsert=False)
    return item                 
