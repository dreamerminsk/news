from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.background import BackgroundTasks
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pymongo import MongoClient
from datetime import datetime, timedelta
import requests
import xml.etree.ElementTree as etree
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

templates = Jinja2Templates(directory='templates')

client = MongoClient()
news = client.news
feeds = news.feeds
articles = news.articles

async def news(request):
    arts = articles.find({}).sort([("published", -1)]).limit(64)
    return templates.TemplateResponse('news.html', {'request': request, 'articles': arts})


async def show_feeds(request):
    arts = feeds.find({}).sort([("ttl", 1)])
    #for art in arts:
        #art['ttlf'] = str(art['ttl'])
    return templates.TemplateResponse('feeds.html', {'request': request, 'feeds': arts})

class FeedEndpoint(HTTPEndpoint):
    async def get(self, request):
        feed_id = request.path_params['feed_id']
        feed = feeds.find_one({"_id": ObjectId(feed_id)})
        feed['_id'] = str(feed['_id'])
        feed['last_access'] = str(feed['last_access'])
        feed['next_access'] = str(feed['next_access'])
        feed['ttlf'] = str(feed['ttl'])
        return JSONResponse(feed)

async def update_feeds(request):
    tasks = BackgroundTasks()
    ids = []
    for feed in feeds.find({"next_access": {"$lte": datetime.now()}}):
        ids.append(str(feed['_id']))
        tasks.add_task(update_feed, feed)
    message = {'status': 'Successful', 'ids': ids}
    return JSONResponse(message, background=tasks)

async def update_feed(feed):
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

app = Starlette(debug=True, routes=[
    Route('/', news),
    Route('/news', news),
    Route('/feeds', show_feeds),
    Route('/feeds/update', update_feeds),
    Route('/feeds/{feed_id}', FeedEndpoint),
    Mount('/static', StaticFiles(directory='static'), name='static')
])
