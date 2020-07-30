import asyncio
import pprint
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient

from web import get_text


print = pprint

client = MongoClient()
news = client.news
users = news.users

text = get_text('https://talks.by/showthread.php?t=14464110')
if text:
    soup = BeautifulSoup(text, 'html.parser')
    soup.select('div.row-user a.username')