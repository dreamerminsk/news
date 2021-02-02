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


class NationsEndpoint(HTTPEndpoint):
    async def get(self, request):
        countries = ibustats.countries.find({})
        latest = []
        for country in countries:
            country['_id'] = str(country['_id'])
            if 'last_modified' in country:
                country['last_modified'] = str(country['last_modified'])
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(country)
            latest.append(country)
        return JSONResponse({'status': 'ok', 'countries': latest})

    async def post(self, request):
        pass


class NationEndpoint(HTTPEndpoint):
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
