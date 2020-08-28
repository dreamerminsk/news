from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo import MongoClient

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

client = MongoClient()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        client.stats.hosts.update_one({'host': request.client.host}, {
                                      '$inc': {'requests': 1}}, upsert=True)
        client.stats.hosts.update_one({'host': request.client.host}, {
                                      '$set': {'last': datetime.now()}}, upsert=True)
        client.stats.hosts.update_one({'host': request.client.host}, {
                                      '$set': {'last_path': request.url.path}}, upsert=True)
        return response
