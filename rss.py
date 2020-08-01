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
    {'link': 'https://nn.by/?c=rss-all'},
    {'$set': {
        'title': 'ch',
        'last_access': datetime.now(),
        'next_access': datetime.now() - timedelta(seconds=1000),
        'ttl': 100}},
    upsert=True)


print(feeds.count_documents({}))
