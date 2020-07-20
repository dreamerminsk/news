from starlette.applications import Starlette
from starlette.responses import JSONResponse
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
    article = articles.find({}).sort([("published", -1)]).limit(1)[0]
    article['_id'] = str(article['_id'])
    article['published'] = str(article['published'])
    return JSONResponse(article)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
