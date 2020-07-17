import requests
import xml.etree.ElementTree as etree

r = requests.get('https://news.tut.by/rss/all.rss')
print(r.text)
root = etree.fromstring(r.text)
for child in root:
    print(child.tag, child.attrib)
    for c in child:
        print("    ", c.tag, c.attrib)
