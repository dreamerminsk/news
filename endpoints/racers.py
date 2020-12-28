import asyncio
import pprint
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo import MongoClient

from starlette.endpoints import HTTPEndpoint
from starlette.responses import (JSONResponse, PlainTextResponse,
                                 RedirectResponse)

client = MongoClient()
ibustats = client.ibustats


class RacersEndpoint(HTTPEndpoint):
    async def get(self, request):
        limit = request.path_params['limit']
        limit = 100 if limit is None else limit
        racers = ibustats.racers.find({}).limit(limit)
        latest = []
        for racer in racers:
            racer['_id'] = str(racer['_id'])
            latest.append(racer)
        return JSONResponse({'status': 'ok', 'racers': latest})

    async def post(self, request):
        pass


class RacerEndpoint(HTTPEndpoint):
    async def get(self, request):
        wdid = request.path_params['wikidataid']
        task = ibustats.racers.find_one({'WikiDataID': wdid})
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)

    async def put(self, request):
        pass