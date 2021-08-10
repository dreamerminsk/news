import asyncio
import random
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from pymongo import MongoClient
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from endpoints.admin import AdminView, DbEndpoint, DbsEndpoint, CollEndpoint, CollsEndpoint
from endpoints.news import (FeedEndpoint, FeedSourceEndpoint,
                            RssReaderEndpoint, TaskEndpoint, XmlEditorEndpoint)
from middleware.logging import LoggingMiddleware
from workers.web import get_text, get_text_async
from workers.wiki import (get_externals, get_info, process_countries,
                          process_seasons)

#print = pprint.pprint

templates = Jinja2Templates(directory='templates')

client = MongoClient()
news = client.news
feeds = news.feeds
articles = news.articles
users = news.users


async def show(request):
    return RedirectResponse(url='/view/feeds')


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

# db.collectionName.aggregate([{$project: {field1_you_need_in_result: 1,field12_you_need_in_result: 1,your_year_variable: {$year: '$your_date_field'}, your_month_variable: {$month: '$your_date_field'}}},{$match: {your_year_variable:2017, your_month_variable: 3}}]);


async def show_users(request):
    user_list = users.find({}).limit(32)
    letter_list = users.aggregate(
        [{
            '$project':
         {
             'uname': {'$toUpper': '$name'}
         }
         },
            {
                '$group':
            {
                '_id': {'$substrCP': ['$uname', 0, 1]}, 'count': {'$sum': 1}}
        },
            {
                '$sort': {'_id': 1}
        }
        ])
    fds = [user for user in user_list]
    return templates.TemplateResponse('users.html', {
        'request': request, 'counts': letter_list, 'letters': letter_list, 'users': fds})


async def show_hosts(request):
    host_stats = client.stats.hosts.find({})
    hosts = [host for host in host_stats]
    return templates.TemplateResponse('hosts.html', {'request': request, 'hosts': hosts})


async def latest_feeds(request):
    latest = []
    for feed in feeds.find({"last_access": {"$gte": datetime.now() - timedelta(seconds=600)}}):
        feed['_id'] = str(feed['_id'])
        feed['last_access'] = str(feed['last_access'])
        feed['next_access'] = str(feed['next_access'])
        feed['ttlf'] = str(timedelta(seconds=feed['ttl']))
        latest.append(feed)
    return JSONResponse({'status': 'ok', 'feeds': latest})


async def start_job():
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(process_countries()),
             loop.create_task(queue_wiki_info()),
             loop.create_task(process_players()),
             loop.create_task(process_policlinics()),
             loop.create_task(process_seasons())]


middleware = [
    Middleware(LoggingMiddleware)
]

app = Starlette(debug=True, routes=[
    Route('/api/feeds/latest', latest_feeds),
    Route('/api/feeds/{feed_id}', FeedEndpoint),
    Route('/api/feeds/{feed_id}/source', FeedSourceEndpoint),
    Route('/api/tasks/{name}', TaskEndpoint),

    Route('/reader/feeds/{feed_id}', RssReaderEndpoint),
    Route('/editor/feeds/{feed_id}', XmlEditorEndpoint),

    Route('/', show_news),
    Route('/view/news', show_news),
    Route('/view/feeds', show_feeds),
    Route('/view/users', show_users),
    Route('/view/hosts', show_hosts),

    Route('/api/admin/dbs', DbsEndpoint),
    Route('/api/admin/dbs/{db}', DbEndpoint),
    Route('/api/admin/dbs/{db}/colls', CollsEndpoint),
    Route('/api/admin/dbs/{db}/colls/{coll}', CollEndpoint),

    Route('/admin/{rest_of_path:path}', AdminView),

    Mount('/static', StaticFiles(directory='static'), name='static')
], middleware=middleware, on_startup=[start_job])
