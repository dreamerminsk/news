from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pymongo import MongoClient
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup

templates = Jinja2Templates(directory='templates')


async def homepage(request):
    client = MongoClient()
    news = client.news
    articles = news.articles
    arts = articles.find({}).sort([("published", -1)]).limit(64)
    text = ''
    for art in arts:
        text += art['title'] + '\r\n'
        text += str(art['published']) + '\r\n'
        text += '\r\n'
    return PlainTextResponse(text)


async def news(request):
    client = MongoClient()
    news = client.news
    articles = news.articles
    arts = articles.find({}).sort([("published", -1)]).limit(64)
    return templates.TemplateResponse('news.html', {'request': request, 'articles': arts})


async def feeds(request):
    client = MongoClient()
    news = client.news
    feeds = news.feeds
    arts = feeds.find({})
    return templates.TemplateResponse('feeds.html', {'request': request, 'feeds': arts})

async def update_feeds(request):
    task = BackgroundTask(uf)
    message = {'status': 'Signup successful'}
    return JSONResponse(message, background=task)

async def uf():
    client = MongoClient()
    news = client.news
    feeds = news.feeds
    arts = feeds.find({})
    for feed in feeds.find({"next_access": {"$lte": datetime.now()}}):
        print(feed)
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
                         '$set': {'next_access': datetime.now() + timedelta(seconds=0.9 * feed['ttl'])
                                 }}, upsert=False)
        else:
            feeds.update_one({'_id': feed['_id']}, {
                         '$set': {'ttl': 1.1 * feed['ttl']}}, upsert=False)
            feeds.update_one({'_id': feed['_id']}, {
                         '$set': {'next_access': datetime.now() + timedelta(seconds=1.1 * feed['ttl'])
                                 }}, upsert=False)

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/news', news),
    Route('/feeds', feeds),
    Route('/feeds/update', update_feeds),
])
