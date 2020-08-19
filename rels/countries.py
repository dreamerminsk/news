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


class CountriesEndpoint(HTTPEndpoint):
    async def get(self, request):
        task = rels.countries.find({})
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)
      
    async def post(self, request):
        country = await request.json()
        rels.countries.update_one({'WikiDataID': country['WikiDataID']}, {'Name': country['Name'], 'RusName': country['RusName'],}, upsert=True)
        return JSONResponse({'result': 'ok'}, status_code=201)
      
      
      
class CountryEndpoint(HTTPEndpoint):
    async def get(self, request):
        wdid = request.path_params['wikidataid']
        task = rels.countries.find_one({'WikiDataID': wdid})
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)
      
    async def put(self, request):
        pass
