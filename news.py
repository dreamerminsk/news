from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from pymongo import MongoClient
from datetime import datetime


client = MongoClient()
news = client.news
articles = news.articles
feeds = news.feeds


async def homepage(request):
    client = MongoClient()
    news = client.news
    articles = news.articles
    now = datetime.now()
    nowp1 = datetime.now() + datetime.timedelta(days=1)
    article = articles.find_one({"published": {"gte": datetime(now.year, now.month, now.day), "lt": datetime(nop1.year, nowp1.month, nowp1.day)}})
    article['_id'] = str(article['_id'])
    article['published'] = str(article['published'])
    return JSONResponse(article)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
