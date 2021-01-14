import asyncio
import pprint
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
from starlette.applications import Starlette
from starlette.background import BackgroundTask, BackgroundTasks
from starlette.middleware import Middleware
from starlette.responses import (JSONResponse, PlainTextResponse,
                                 RedirectResponse)
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from endpoints.news import RssReaderEndpoint, XmlEditorEndpoint, FeedEndpoint, FeedSourceEndpoint, TaskEndpoint
from endpoints.racers import NamesEndpoint, RacersEndpoint
from endpoints.seasons import SeasonsEndpoint
from middleware.logging import LoggingMiddleware
from rels.countries import CountriesEndpoint, CountryEndpoint
from rels.humans import HumanEndpoint, HumansEndpoint
from rels.instances import InstanceEndpoint, InstancesEndpoint
from workers.web import get_text
from workers.wiki import get_category, get_info, get_links, get_pages

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


async def show_rels(request):
    return templates.TemplateResponse('rels.html', {'request': request})


async def show_instances(request):
    instances = client.rels.instances.find({})
    return templates.TemplateResponse('instances.html', {'request': request, 'instances': instances})


async def show_countries(request):
    countries = client.rels.countries.find({})
    return templates.TemplateResponse('countries.html', {'request': request, 'countries': countries})


async def show_categories(request):
    categories = client.rels.categories.find({})
    return templates.TemplateResponse('categories.html', {'request': request, 'categories': categories})


async def show_ibu(request):
    return templates.TemplateResponse('ibustats.html', {'request': request})


async def show_ibu_countries(request):
    return templates.TemplateResponse('ibucountries.html', {'request': request})


async def show_ibu_seasons(request):
    return templates.TemplateResponse('ibuseasons.html', {'request': request})


async def show_feeds(request):
    arts = feeds.find({}).sort([("ttl", 1)])
    fds = []
    for art in arts:
        art['ttlf'] = str(timedelta(seconds=art['ttl']))
        fds.append(art)
    return templates.TemplateResponse('feeds.html', {'request': request, 'feeds': fds})


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
    fds = []
    for user in user_list:
        fds.append(user)
    return templates.TemplateResponse('users.html', {
        'request': request, 'counts': letter_list, 'letters': letter_list, 'users': fds})


async def show_hosts(request):
    host_stats = client.stats.hosts.find({})
    hosts = []
    for host in host_stats:
        hosts.append(host)
    return templates.TemplateResponse('hosts.html', {'request': request, 'hosts': hosts})


async def show_talks(request):
    return templates.TemplateResponse('talks.html', {'request': request})


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
    count = articles.count_documents({})
    print('{}. {}'.format(datetime.now(), count))
    news.tasks.update_one({'name': 'feeds'}, {
        '$set': {'start': datetime.now(), 'feeds': 0, 'articles': count}}, upsert=True)
    # feeds.update_one({'link': 'http://www.filmz.ru/rss/files/rambler.xml'}, {
    #   '$set': {'last_access': datetime.now(), 'next_access': datetime.now(), 'ttl': 1000}}, upsert=True)
    q = asyncio.Queue()
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(queue_feeds(q)),
             loop.create_task(process_feeds(q)),
             loop.create_task(queue_wiki_info())]


async def queue_wiki_info():
    racers = client.ibustats.racers.find({})
    wikis = []
    for racer in racers:
        wikis.append(racer['wiki']['ru'])
    for wiki in wikis:
        info = await get_info('ru', wiki)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'countries': info['countries']}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'name': info['name']}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'image': info['image']}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'desc': info['desc']}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'bday': str(info['bday'])}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'last_modified': datetime.now()}}, upsert=False)
        await asyncio.sleep(8)
    await asyncio.sleep(32)


async def queue_feeds(q):
    while True:
        for feed in feeds.find({"next_access": {"$lte": datetime.now()}}):
            await q.put(feed)
        await asyncio.sleep(60)


async def process_feeds(q):
    while True:
        try:
            feed = await q.get()
            await update_feed2(feed)
        finally:
            q.task_done()
            news.tasks.update_one({'name': 'feeds'}, {
                '$inc': {'feeds': 1}}, upsert=True)


async def update_feed2(feed):
    i = 0
    text = get_text(feed['link'])
    if text:
        try:
            root = etree.fromstring(text)
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
        except Exception as e:
            print(feed['link'], e)

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


middleware = [
    Middleware(LoggingMiddleware)
]

app = Starlette(debug=True, routes=[
    Route('/api/humans/', HumansEndpoint),
    Route('/api/rels/humans/{wikidataid}', HumanEndpoint),
    Route('/api/rels/countries', CountriesEndpoint),
    Route('/api/rels/countries/{wikidataid}', CountryEndpoint),
    Route('/api/rels/instances', InstancesEndpoint),
    Route('/api/rels/instances/{wikidataid}', InstanceEndpoint),

    Route('/api/feeds/latest', latest_feeds),
    Route('/api/feeds/{feed_id}', FeedEndpoint),
    Route('/api/feeds/{feed_id}/source', FeedSourceEndpoint),
    Route('/api/tasks/{name}', TaskEndpoint),

    Route('/reader/feeds/{feed_id}', RssReaderEndpoint),
    Route('/editor/feeds/{feed_id}', XmlEditorEndpoint),

    Route('/', show),
    Route('/view/news', show_news),
    Route('/view/feeds', show_feeds),
    Route('/view/users', show_users),
    Route('/view/hosts', show_hosts),

    Route('/view/rels', show_rels),
    Route('/view/instances', show_instances),
    Route('/view/countries', show_countries),
    Route('/view/categories', show_categories),


    Route('/api/ibu/racers', RacersEndpoint),
    Route('/api/ibu/racers/names/{startswith}', NamesEndpoint),
    Route('/api/ibu/seasons', SeasonsEndpoint),

    Route('/view/ibu', show_ibu),
    Route('/view/ibu/racers', show_ibu),
    Route('/view/ibu/countries', show_ibu_countries),
    Route('/view/ibu/seasons', show_ibu_seasons),

    Route('/view/talksby', show_talks),

    Mount('/static', StaticFiles(directory='static'), name='static')
], middleware=middleware, on_startup=[start_job])
