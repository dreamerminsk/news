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

for feed in feeds.find():
    print(feed)
    diff = datetime.now() - feed['last_access']
    if diff.seconds > 900:
        i = 0
        r = requests.get(feed['link'])
        root = etree.fromstring(r.text)
        for channel in root.findall('channel'):
            feeds.update_one({'_id': feed['_id']}, {
                             '$set': {'title': channel.find('title').text}}, upsert=False)
            print(channel.find('title').text)
            feeds.update_one({'_id': feed['_id']}, {
                             '$set': {'description': channel.find('description').text}}, upsert=False)
            print(channel.find('description').text)
            for item in channel.findall('item'):
                title = item.find('title').text
                link = item.find('link').text
                if '?' in link:
                    link = link[:link.find('?')]
                pub = item.find('pubDate').text
                if not articles.find_one({"link": link}):
                    i += 1
                    articles.insert_one({"link": link, "title": title})
                    print(i)
                    print(title)
                    print(link)
                    print(pub)
        feeds.update_one({'_id': feed['_id']}, {
                         '$set': {'last_access': datetime.now()}}, upsert=False)
        if i > 0:
            feeds.update_one({'_id': feed['_id']}, {
                             '$set': {'ttl': 0.9 * feed['ttl']}}, upsert=False)
            feeds.update_one({'_id': feed['_id']}, {
                             '$set': {'next_access': datetime.now()}}, upsert=False)
        else:
            feeds.update_one({'_id': feed['_id']}, {
                             '$set': {'ttl': 1.1 * feed['ttl']}}, upsert=False)
            feeds.update_one({'_id': feed['_id']}, {
                             '$set': {'next_access': datetime.now()}}, upsert=False)

n = 0
total = articles.find()
for item in total:
    if 'thread' not in item:
        print(item)
        if 'tut.by' in item['link']:
            if 'm.tut.by' in item['link']:
                continue
            if 'tut.by/pda/' in item['link']:
                continue
            if n > 32:
                break
            p = requests.get(item['link'])
            soup = BeautifulSoup(p.text, "html.parser")
            title = soup.select_one(
                'div.b-article div.m_header h1[itemprop="headline"]')
            print('***************************************************')
            print('?' if title is None else title.text)
            t = soup.select_one('p.b-article-details time')
            dt = datetime(1, 1, 1, 0, 0, 0) if t is None else datetime.strptime(
                t.get('datetime'), '%Y-%m-%dT%H:%M:%S%z')
            print('published: {0}'.format(dt))
            articles.update_one({'_id': item['_id']}, {
                                '$set': {'published': dt}}, upsert=False)
            cc = soup.select_one('span[itemprop="commentCount"]')
            print('comments: {0}'.format(0 if cc is None else int(cc.text)))
            articles.update_one({'_id': item['_id']}, {
                                '$set': {'comments': 0 if cc is None else int(cc.text)}}, upsert=False)
            th = soup.select_one('div.b-comments a.b-add_comments')
            print('thread: {0}'.format('' if th is None else th.get('href')))
            articles.update_one({'_id': item['_id']}, {
                                '$set': {'thread': '' if th is None else th.get('href')}}, upsert=False)
            n += 1
print('***************************************************')
print('articles: {}'.format(articles.count_documents({})))
print('{}'.format(news.command('dbstats')))
