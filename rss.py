import requests
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

print = pprint.pprint

client = MongoClient()
news = client.news
feeds = news.feeds

r = requests.get('https://news.tut.by/rss.html')
soup = BeautifulSoup(r.text, "html.parser")
links = soup.select('li.lists__li a')
for link in links:
    if link.get('href').endswith('.rss'):
        print(link.text)
        print(link.get('href'))
        feeds.update_one({'link': link.get('href')}, {
                         '$set': {'title': link.text, 'ttl': 100}}, upsert=True)


r = requests.get('https://www.onliner.by')
soup = BeautifulSoup(r.text, "html.parser")
links = soup.select('a[href]')
for link in links:
    if link.get('href').endswith('feed'):
        print(link.text)
        print(link.get('href'))
        feeds.update_one({'link': link.get('href')}, {
                         '$set': {'title': link.text, 'ttl': 100}}, upsert=True)


feeds.update_one(
    {'link': 'https://www.eurosport.ru/rss.xml'},
    {'$set': {
        'title': 'ch',
        'last_access': datetime.now(),
        'next_access': datetime.now() - timedelta(seconds=1000),
        'ttl': 100}},
    upsert=True)


print(feeds.count_documents({}))
