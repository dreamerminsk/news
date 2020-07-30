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

client = MongoClient()
news = client.news
users = news.users

text = get_text('https://talks.by/showthread.php?t=14464110')
if text:
    soup = BeautifulSoup(text, 'html.parser')
    user_nodes = soup.select('div.row-user a.username')
    if user_nodes:
        for user_node in user_nodes:
            query = parse.urlsplit(user_node.get('abs:href')).query
            params = parse.parse_qs(query)
            print(user_node.text)
            print(user_node.get('abs:href'))
            print(user_node.params['u'][0])