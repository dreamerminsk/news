import pprint
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

print = pprint.pprint

client = MongoClient()
news = client.news
articles = news.articles
feeds = news.feeds

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
