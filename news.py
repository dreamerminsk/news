from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.background import BackgroundTasks
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pymongo import MongoClient
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from fake_useragent import UserAgent
import asyncio

templates = Jinja2Templates(directory='templates')

client = MongoClient()
news = client.news
feeds = news.feeds
articles = news.articles


async def show_news(request):
    arts = articles.find({}).sort([("published", -1)]).limit(64)
    return templates.TemplateResponse('news.html', {'request': request, 'articles': arts})


async def show_feeds(request):
    arts = feeds.find({}).sort([("ttl", 1)])
    fds = []
    for art in arts:
        art['ttlf'] = str(timedelta(seconds=art['ttl']))
        fds.append(art)
    return templates.TemplateResponse('feeds.html', {'request': request, 'feeds': fds})


class FeedEndpoint(HTTPEndpoint):
    async def get(self, request):
        feed_id = request.path_params['feed_id']
        feed = feeds.find_one({"_id": ObjectId(feed_id)})
        feed['_id'] = str(feed['_id'])
        feed['last_access'] = str(feed['last_access'])
        feed['next_access'] = str(feed['next_access'])
        feed['ttlf'] = str(timedelta(seconds=feed['ttl']))
        return JSONResponse(feed)


class TaskEndpoint(HTTPEndpoint):
    async def get(self, request):
        host = request.path_params['host']
        task = news.tasks.find_one({"host": host})
        if task is not None:
            task['_id'] = str(task['_id'])
            task['start'] = str(task['start'])
        else:
            task = {
                'idx': 0,
                'host': host,
                'rss': 0,
                'rss_total': 0,
            }
        return JSONResponse(task)


async def update_feeds(request):
    tasks = BackgroundTasks()
    ids = []
    for feed in feeds.find({"next_access": {"$lte": datetime.now()}}):
        ids.append(str(feed['_id']))
        tasks.add_task(update_feed, feed)
    news.tasks.update_one({'host': str(request.client.host)},
                          {'$set': {'start': datetime.now()}}, upsert=True)
    news.tasks.update_one({"host": str(request.client.host)},
                          {'$set': {'rss': len(ids)}}, upsert=True)
    news.tasks.update_one({"host": str(request.client.host)},
                          {'$set': {'ids': ids}}, upsert=True)
    news.tasks.update_one({"host": str(request.client.host)},
                          {'$inc': {'idx': 1, 'rss_total': len(ids)}}, upsert=True)
    return RedirectResponse(url='/tasks/{}'.format(request.client.host), background=tasks)


async def update_feed(feed):
    print(feed)
    i = 0
    r = requests.get(feed['link'], headers={'User-Agent': UserAgent().random})
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
            print('{}. {}'.format(i, title))
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

async def start_job():
    await long_job()

async def long_job():
    for i in range(32):
        count = articles.count_documents({})
        news.tasks.update({}, {'articles': count})
        await asyncio.sleep(60)
      

app = Starlette(debug=True, routes=[
    Route('/', show_news),
    Route('/news', show_news),
    Route('/feeds', show_feeds),
    Route('/feeds/update', update_feeds),
    Route('/feeds/{feed_id}', FeedEndpoint),
    Route('/tasks/{host}', TaskEndpoint),
    Mount('/static', StaticFiles(directory='static'), name='static')
], on_startup=[start_job])
