from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from pymongo import MongoClient
from datetime import datetime, timedelta


client = MongoClient()
news = client.news
articles = news.articles
feeds = news.feeds


async def homepage(request):
    client = MongoClient()
    news = client.news
    articles = news.articles
    arts = articles.find({}).sort([("published", -1)]).limit(16)
    text = ''
    for art in arts:
        text += art['title'] + '\r\n'
        text += art['published'] + '\r\n'
        text += '\r\n'
    return PlainTextResponse(text)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
