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


class CountriesEndpoint(HTTPEndpoint):
    async def get(self, request):
        racers = ibustats.countries.find({})
        latest = []
        for racer in racers:
            racer['_id'] = str(racer['_id'])
            if 'last_modified' in racer:
                racer['last_modified'] = str(racer['last_modified'])
            latest.append(racer)
        return JSONResponse({'status': 'ok', 'countries': latest})

    async def post(self, request):
        pass


class CountryEndpoint(HTTPEndpoint):
    async def get(self, request):
        wdid = request.path_params['wikidataid']
        task = ibustats.countries.find_one({'WikiDataID': wdid})
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)

    async def put(self, request):
        pass
