from pymongo import MongoClient
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from fake_useragent import UserAgent
import asyncio

async def parse(text):
    root = etree.fromstring(text)
    for channel in root.findall('channel'):
        for item in channel.findall('item'):
            article = await parse_item(item)


async def parse_item(item):
    title = item.find('title').text
        link = item.find('link').text
        if '?' in link:
            link = link[:link.find('?')]
        if not articles.find_one({"link": link}):
            articles.insert_one({"link": link, "title": title})
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
