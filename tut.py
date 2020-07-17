import requests
import xml.etree.ElementTree as etree

r = requests.get('https://news.tut.by/rss/all.rss')
root = etree.fromstring(r.text)
for child in root:
    print(child.tag, child.attrib)
    for item in child:
        print("    ", item.tag, item.attrib)
        for c in item:
            print("        ", c.tag, c.attrib)
