from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo import MongoClient

from starlette.templating import Jinja2Templates

from starlette.endpoints import HTTPEndpoint
from starlette.responses import (JSONResponse, PlainTextResponse,
                                 RedirectResponse)


client = MongoClient()
news = client.news
feeds = news.feeds
articles = news.articles
users = news.users


templates = Jinja2Templates(directory='templates')


class FeedEndpoint(HTTPEndpoint):
    async def get(self, request):
        feed_id = request.path_params['feed_id']
        feed = feeds.find_one({"_id": ObjectId(feed_id)})
        feed['_id'] = str(feed['_id'])
        feed['last_access'] = str(feed['last_access'])
        feed['next_access'] = str(feed['next_access'])
        feed['ttlf'] = str(timedelta(seconds=feed['ttl']))
        return JSONResponse(feed)
      
class FeedSourceEndpoint(HTTPEndpoint):
    async def get(self, request):
        feed_id = request.path_params['feed_id']
        feed = feeds.find_one({"_id": ObjectId(feed_id)})
        text = get_text(feed['link'])
        return PlainTextResponse(text, media_type='text/plain')


class RssReaderEndpoint(HTTPEndpoint):
    async def get(self, request):
        feed_id = request.path_params['feed_id']
        feed = feeds.find_one({"_id": ObjectId(feed_id)})
        return templates.TemplateResponse('rss-reader.html', {'request': request, 'feed': feed})


class XmlEditorEndpoint(HTTPEndpoint):
    async def get(self, request):
        feed_id = request.path_params['feed_id']
        feed = feeds.find_one({"_id": ObjectId(feed_id)})
        return templates.TemplateResponse('xml-editor.html', {'request': request, 'feed': feed})


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
