import asyncio
import pprint
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta
from urllib import parse

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient

from web import get_text

#print = pprint
pp = pprint.PrettyPrinter(indent=4)

client = MongoClient()
news = client.news
users = news.users
threads = news.threads

turls = set()

urls = set()

for i in range(8):
    turls.add('https://talks.by/forumdisplay.php?f=45&page={}&order=desc'.format(i))

while len(turls) > 0:
    turl = turls.pop()
    print(turl)
    threads_page = get_text(turl)
    if threads_page:
        soup = BeautifulSoup(threads_page, 'html.parser')
        ref_nodes = soup.select('a[href]')
        if ref_nodes:
            for ref_node in ref_nodes:
                query = parse.urlsplit(ref_node.get('href')).query
                params = parse.parse_qs(query)
                if 't' in params:
                    thread_url = 'https://talks.by/showthread.php?t={}'.format(
                        params['t'][0])
                    if thread_url not in urls:
                        print('{}. {}'.format(params['t'][0], ref_node.text))
                        urls.add(thread_url)
                        threads.update_one({'thread_id': params['t'][0]}, {
                                           '$set': {'title': ref_node.text}}, upsert=True)
    print(len(urls))

print(threads.count_documents({}))
