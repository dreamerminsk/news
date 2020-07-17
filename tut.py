import requests
import xml.etree.ElementTree as etree

r = requests.get('https://news.tut.by/rss/all.rss')
print(r.text)
tree = etree.parse(r.text)
root = tree.getroot()
print(root)
