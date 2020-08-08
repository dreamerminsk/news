# table.themaCommentTable
# tr
# td.themaCommentLeft
# div.rowUser id > a.postuseravatar > img, a.username
# td.themaCommentRight
#     a.name
#     div.row-content-date
#       Добавлено: Сегодня 08:29 из Беларуси
#       Добавлено: 19.07.20 12:39 из Беларуси
#       link_rate_up link_rate_down


import asyncio
import pprint
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient

from web import get_text
from urllib import parse


client = MongoClient()
news = client.news
users = news.users
threads = news.threads

urls = set()

threads4 = threads.find({}).sort([("thread_id", 1)]).limit(32)
for thread in threads4:
    thread_url = 'https://talks.by/showthread.php?t={}'.format(
        thread['thread_id'])
    urls.add(thread_url)


def parse_user(node):


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
                if op_result.upserted_id:
                    print('\t{} - {}'.format(params['u'][0], user_node.text))
print(users.count_documents({}))
