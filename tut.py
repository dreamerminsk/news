import datetime
import requests
import xml.etree.ElementTree as etree
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup

print = pprint.pprint

client = MongoClient()
news = client.news
articles = news.articles

r = requests.get('https://news.tut.by/rss/all.rss')
root = etree.fromstring(r.text)
i = 0
for channel in root.findall('channel'):
    for item in channel.findall('item'):
        i += 1
        title = item.find('title').text
        link = item.find('link').text
        if '?' in link:
            link = link[:link.find('?')]
        pub = item.find('pubDate').text
        if not articles.find_one({"link":link}):
            articles.insert_one({"link":link,"title":title})
            print(i)
            print(title)
            print(link)
            print(pub)

total = articles.find()
for item in total:
    if 'published' not in item:
        print(item)
        p = requests.get(item['link'])
        soup = BeautifulSoup(p.text, "html.parser", convertEntities=BeautifulSoup.HTML_ENTITIES)
        title = soup.select_one('div.b-article div.m_header h1[itemprop="headline"]')
        print(title.text)
        t = soup.select_one('p.b-article-details time')
        dt = datetime.datetime.strptime(t.get('datetime'), '%Y-%m-%dT%H:%M:%S%z')
        print(dt)
        articles.update_one({'_id': item['_id']}, {'$set': {'published': dt}}, upsert=False)
        break
