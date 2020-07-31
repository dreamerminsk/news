import asyncio
import pprint
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient

from web import get_text
from urllib import parse


#print = pprint
pp = pprint.PrettyPrinter(indent=4)

client = MongoClient()
news = client.news
users = news.users

turls = set()

urls = set()

for i in range(64):
    turls.add('https://talks.by/forumdisplay.php?f=160&page={}&order=desc'.format(i))

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
                    urls.add('https://talks.by/showthread.php?t={}'.format(params['t'][0]))
    print(len(urls))

while len(urls) > 0:
    url = urls.pop()
    print(url)
    text = get_text(url)
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        ref_nodes = soup.select('a[href]')
        if ref_nodes:
            for ref_node in ref_nodes:
                if '>>' in ref_node.text:
                    urls.add('https://talks.by/{}'.format(ref_node.get('href')))
        user_nodes = soup.select('div.row-user a.username')
        if user_nodes:
            for user_node in user_nodes:
                query = parse.urlsplit(user_node.get('href')).query
                params = parse.parse_qs(query)
                op_result = users.update_one({'u': params['u'][0]}, {
                    '$set': {'name': user_node.text}}, upsert=True)
                #pp.pprint('{}, {}, {}'.format(op_result.matched_count, op_result.modified_count, op_result.upserted_id))  
                if op_result.upserted_id:
                    print('\t{} - {}'.format(params['u'][0], user_node.text))
print(users.count_documents({}))
