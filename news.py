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
    return JSONResponse(articles.find_one({}))


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
