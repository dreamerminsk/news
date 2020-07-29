import requests
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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


print(feeds.count_documents({}))
