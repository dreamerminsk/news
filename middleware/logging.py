from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo import MongoClient

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

client = MongoClient()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        client.stats.hosts.update_one({ 'host' : request.client.host }, {
                                      '$inc' : { 'requests': 1 } }, upsert=True)
        client.stats.hosts.update_one(
            { 'host': request.client.host }, 
            { '$inc': { 'last-req-count' : 1 }, 
                '$push' : { 'last-requests' : { 'datetime' : 'datetime.now(), 'path' : request.url.path } } 
            }
        )
        client.stats.hosts.update_one(
            { 'host': request.client.host, 'last-req-count' : { '$gt': 3 } }, 
            { '$inc': { 'last-req-count' : -1 }, '$pop' : { 'last-requests' : -1 } }
        )
        return response
