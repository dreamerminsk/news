import pprint
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

print = pprint.pprint

client = MongoClient()
news = client.news
feeds = news.feeds


feeds.update_one(
    {'link': 'https://www.eurosport.ru/rss.xml'},
    {'$set': {
        'title': 'ch',
        'last_access': datetime.now(),
        'next_access': datetime.now() - timedelta(seconds=1000),
        'ttl': 100}},
    upsert=True)

feeds.update_one(
    {'title': 'От застройщика'},
    {'$set': {
        'last_access': datetime.now(),
        'next_access': datetime.now() - timedelta(seconds=1000),
        'ttl': 100}})


print(feeds.count_documents({}))
