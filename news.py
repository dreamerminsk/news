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
        print(art['title'])
        if art['ttl']:
            art['ttlf'] = str(timedelta(seconds=art['ttl']))
        else:
            art['ttlf'] = '0'
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
        name = request.path_params['name']
        task = news.tasks.find_one({"name": name})
        if task is not None:
            task['_id'] = str(task['_id'])
            task['elapsed'] = str(datetime.now() - task['start'])
            task['start'] = str(task['start'])
            task['total'] = articles.count_documents({})
        else:
            task = {
            }
        return JSONResponse(task)


async def latest_feeds(request):
    latest = []
    for feed in feeds.find({"last_access": {"$gte": datetime.now() - timedelta(seconds=600)}}):
        feed['_id'] = str(feed['_id'])
        feed['last_access'] = str(feed['last_access'])
        feed['next_access'] = str(feed['next_access'])
        feed['ttlf'] = str(timedelta(seconds=feed['ttl']))
        latest.append(feed)
    return JSONResponse(latest)


async def start_job():
    count = articles.count_documents({})
    print('{}. {}'.format(datetime.now(), count))
    news.tasks.update_one({'name': 'feeds'}, {
        '$set': {'start': datetime.now(), 'feeds': 0, 'articles': count}}, upsert=True)
    q = asyncio.Queue()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(queue_feeds(q)),
             loop.create_task(process_feeds(q))]


async def queue_feeds(q):
    while True:
        for feed in feeds.find({"next_access": {"$lte": datetime.now()}}):
            await q.put(feed)
        await asyncio.sleep(60)


async def process_feeds(q):
    while True:
        feed = await q.get()
        await update_feed2(feed)
        q.task_done()
        news.tasks.update_one({'name': 'feeds'}, {
            '$inc': {'feeds': 1}}, upsert=True)


async def update_feed2(feed):
    i = 0
    r = requests.get(feed['link'], headers={'User-Agent': UserAgent().random})
    root = etree.fromstring(r.text)
    for channel in root.findall('channel'):
        feeds.update_one({'_id': feed['_id']}, {
            '$set': {'title': channel.find('title').text}}, upsert=False)
    feeds.update_one({'_id': feed['_id']}, {
                     '$set': {'description': channel.find('description').text}}, upsert=False)
    for item in channel.findall('item'):
        title = item.find('title').text
        link = item.find('link').text
        if '?' in link:
            link = link[:link.find('?')]
        if not articles.find_one({"link": link}):
            i += 1
            articles.insert_one({"link": link, "title": title})
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
    Route('/', show_news),
    Route('/news', show_news),
    Route('/feeds', show_feeds),
    Route('/feeds/latest', latest_feeds),
    Route('/feeds/{feed_id}', FeedEndpoint),
    Route('/tasks/{name}', TaskEndpoint),
    Mount('/static', StaticFiles(directory='static'), name='static')
], on_startup=[start_job])
