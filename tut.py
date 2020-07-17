import requests
import xml.etree.ElementTree as etree
from pymongo import MongoClient

r = requests.get('https://news.tut.by/rss/all.rss')
root = etree.fromstring(r.text)
i = 1
for channel in root.findall('channel'):
    for item in channel.findall('item'):
        i += 1
        title = item.find('title').text
        print(i, title)
            
client = MongoClient()
print(client.news)
