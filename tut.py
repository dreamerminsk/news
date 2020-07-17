import requests
import xml.etree.ElementTree as etree
from pymongo import MongoClient

r = requests.get('https://news.tut.by/rss/all.rss')
root = etree.fromstring(r.text)
i = 0
for channel in root.findall('channel'):
    for item in channel.findall('item'):
        i += 1
        print(i)
        title = item.find('title').text
        print(title)
        link = item.find('link').text
        print(link)
        pub = item.find('pubDate').text
        print(pub)
            
client = MongoClient()
print(client.news)
