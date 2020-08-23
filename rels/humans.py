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
        limit = request.path_params['name']
        task = rels.humans.find_one({}).limit(limit)
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)

    async def post(self, request):
        human = await request.json()
        rels.humans.update_one({'WikiDataID': human['WikiDataID']}, {'$set': {
            'Name': human['Name'], 'RusName': human['RusName'], }}, upsert=True)
        return JSONResponse({'result': 'ok'}, status_code=201)


class HumanEndpoint(HTTPEndpoint):
    async def get(self, request):
        wdid = request.path_params['wikidataid']
        task = rels.humans.find_one({'WikiDataID': wdid})
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)

    async def put(self, request):
        pass
