import requests
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup

print = pprint.pprint

client = MongoClient()
news = client.news
articles = news.articles

r = requests.get('https://news.tut.by/rss.html')
soup = BeautifulSoup(r.text, "html.parser")
feeds = soup.select('li.lists__li a')
for feed in feeds:
    print(feed.text)
    print(feed.get('href'))
