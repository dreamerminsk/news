import requests
import xml.etree.ElementTree as etree
from pymongo import MongoClient

r = requests.get('https://news.tut.by/rss/all.rss')
root = etree.fromstring(r.text)
for channel in root.findall('channel'):
    for item in channel.findall('item'):
        title = country.find('title').text
        print(title)
            
client = MongoClient()
print(client.news)
