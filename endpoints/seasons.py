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


class SeasonsEndpoint(HTTPEndpoint):
    async def get(self, request):
        seasons = ibustats.seasons.find({})
        latest = []
        for season in seasons:
            season['_id'] = str(season['_id'])
            latest.append(season)
        return JSONResponse({'status': 'ok', 'seasons': latest})

    async def post(self, request):
        pass


class SeasonEndpoint(HTTPEndpoint):
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
