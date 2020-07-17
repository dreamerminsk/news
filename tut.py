import requests
import xml.etree.ElementTree as etree

r = requests.get('https://news.tut.by/rss/all.rss')
print(r.text)
root = etree.fromstring(r.text)
print(root)
