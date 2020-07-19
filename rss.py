import requests
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup

print = pprint.pprint

client = MongoClient()
news = client.news
feeds = news.feeds

r = requests.get('https://news.tut.by/rss.html')
soup = BeautifulSoup(r.text, "html.parser")
links = soup.select('li.lists__li a')
for link in links:
    print(link.text)
    print(link.get('href'))
    feeds.update_one({'link': link.get('href')}, {'$set': {'title': link.text}}, upsert=True)
    
for feed in feeds.find():
    print(feed)
