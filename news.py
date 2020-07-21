from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pymongo import MongoClient
from datetime import datetime, timedelta

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
    arts = feeds.find({}).sort([("published", -1)]).limit(64)
    return templates.TemplateResponse('news.html', {'request': request, 'articles': arts})

async def feeds(request):
    client = MongoClient()
    news = client.news
    feeds = news.feeds
    arts = articles.find({})
    return templates.TemplateResponse('feeds.html', {'request': request, 'feeds': arts})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/news', news),
    Route('/feeds', feeds),
])
