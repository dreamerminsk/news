import asyncio
import pprint
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo import MongoClient

from starlette.endpoints import HTTPEndpoint
from starlette.responses import (JSONResponse, PlainTextResponse,
                                 RedirectResponse)

client = MongoClient()
rels = client.rels


class HumansEndpoint(HTTPEndpoint):
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
