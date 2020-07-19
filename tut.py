from datetime import datetime
import requests
import xml.etree.ElementTree as etree
from pymongo import MongoClient
import pprint
from bs4 import BeautifulSoup

print = pprint.pprint

client = MongoClient()
news = client.news
articles = news.articles
feeds = news.feeds

i = 0
for feed in feeds.find():
    print(feed)
    diff = datetime.now() - feed['last_access']
    if diff.seconds > 900:
        r = requests.get(feed['link'])
        root = etree.fromstring(r.text)
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
        feeds.update_one({'_id': feed['_id']}, {'$set': {'last_access': datetime.now()}}, upsert=False)

total = articles.find()
for item in total:
    if 'thread' not in item:
        print(item)
        if 'tut.by' in item['link']:
            p = requests.get(item['link'])
            soup = BeautifulSoup(p.text, "html.parser")
            title = soup.select_one('div.b-article div.m_header h1[itemprop="headline"]')
            print(title.text)
            t = soup.select_one('p.b-article-details time')
            dt = datetime.strptime(t.get('datetime'), '%Y-%m-%dT%H:%M:%S%z')
            print('published: {0}'.format(dt))
            articles.update_one({'_id': item['_id']}, {'$set': {'published': dt}}, upsert=False)
            cc = soup.select_one('span[itemprop="commentCount"]')
            print('comments: {0}'.format(0 if cc is None else int(cc.text)))
            articles.update_one({'_id': item['_id']}, {'$set': {'comments': 0 if cc is None else int(cc.text)}}, upsert=False)
            th = soup.select_one('div.b-comments a')
            print('thread: {0}'.format('' if th is None else th.get('href')))
            articles.update_one({'_id': item['_id']}, {'$set': {'thread': '' if th is None else th.get('href')}}, upsert=False)
            break
print(client)
