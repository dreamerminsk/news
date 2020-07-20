from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from pymongo import MongoClient


client = MongoClient()
news = client.news
articles = news.articles
feeds = news.feeds


async def homepage(request):
    client = MongoClient()
    news = client.news
    articles = news.articles
    article = articles.find_one({})
    article['_id'] = str(article['_id'])
    article['published'] = str(article['published'])
    return JSONResponse(article)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
