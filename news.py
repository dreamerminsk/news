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

from endpoints.admin import AdminView, DbEndpoint, DbsEndpoint
from endpoints.countries import NationEndpoint, NationsEndpoint
from endpoints.news import (FeedEndpoint, FeedSourceEndpoint,
                            RssReaderEndpoint, TaskEndpoint, XmlEditorEndpoint)
from endpoints.racers import (BirthdatesEndpoint, NamesEndpoint,
                              RacersEndpoint, YearMonthEndpoint)
from endpoints.seasons import SeasonsEndpoint
from middleware.logging import LoggingMiddleware
from rels.countries import CountriesEndpoint, CountryEndpoint
from rels.humans import HumanEndpoint, HumansEndpoint
from rels.instances import InstanceEndpoint, InstancesEndpoint
from workers.championat import process_players
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
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(process_countries()),
             loop.create_task(queue_wiki_info()),
             loop.create_task(process_players()),
             loop.create_task(process_seasons())]


async def queue_wiki_info():
    racers = client.ibustats.racers.find({})
    wikis = [racer['wiki']['ru'] for racer in racers]
    random.shuffle(wikis)
    for wiki in wikis:
        info = await get_externals('ru', wiki)
        for external in info['externals']:
            client.ibustats.racers.update_one({'wiki.ru': wiki}, {
                '$addToSet': {'externals': external}}, upsert=False)
    for wiki in wikis:
        info = await get_info('ru', wiki)
        for country in info['countries']:
            client.ibustats.racers.update_one({'wiki.ru': wiki}, {
                '$addToSet': {'countries': country}}, upsert=False)
            client.ibustats.countries.update_one({'wiki.ru': country}, {
                '$set': {'last_modified': datetime.now()}}, upsert=True)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'name': info['name']}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'image': info['image']}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$addToSet': {'images': info['image']}}, upsert=False)
        if info['desc']:
            client.ibustats.racers.update_one({'wiki.ru': wiki}, {
                '$set': {'desc': info['desc']}}, upsert=False)
        if info['bday']:
            client.ibustats.racers.update_one({'wiki.ru': wiki}, {
                '$set': {'bday': str(info['bday'])}}, upsert=False)
        client.ibustats.racers.update_one({'wiki.ru': wiki}, {
            '$set': {'last_modified': datetime.now()}}, upsert=False)
        await asyncio.sleep(4 + random.randint(4, 12))
    await asyncio.sleep(32)


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

    Route('/', show_ibu),
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
    Route('/api/ibu/racers/year/{year}/month/{month}', YearMonthEndpoint),
    Route('/api/ibu/seasons', SeasonsEndpoint),
    Route('/api/ibu/countries', NationsEndpoint),
    Route('/api/ibu/countries/{wikidataid}', NationEndpoint),


    Route('/view/ibu', show_ibu),
    Route('/view/ibu/racers', show_ibu),
    Route('/view/ibu/countries', show_ibu_countries),
    Route('/view/ibu/seasons', show_ibu_seasons),
    Route('/view/ibu/birthdates', BirthdatesEndpoint),

    Route('/api/admin/dbs', DbsEndpoint),
    Route('/api/admin/dbs/{name}', DbEndpoint),

    Route('/view/admin', AdminView),

    Mount('/static', StaticFiles(directory='static'), name='static')
], middleware=middleware, on_startup=[start_job])
