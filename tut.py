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
    if 'published' not in item.keys()
        print(item)
        p = requests.get(item['link'])
        soup = BeautifulSoup(p.text)
        t = soup.select_one('p.b-article-details time[@itemprop="datePublished"]')
        print(t)
        break
