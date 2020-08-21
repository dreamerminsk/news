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


class InstancesEndpoint(HTTPEndpoint):
    async def get(self, request):
        latest = []
        for instance in rels.instances.find({}):
            instance['_id'] = str(instance['_id'])
            latest.append(instance)
        return JSONResponse({'status': 'ok', 'instances': latest})
      
    async def post(self, request):
        instance = await request.json()
        rels.instances.update_one({'WikiDataID': instance['WikiDataID']}, {'$set': {'Name': instance['Name'], 'RusName': instance['RusName'],}}, upsert=True)
        return JSONResponse({'result': 'ok'}, status_code=201)
      
      
      
class InstanceEndpoint(HTTPEndpoint):
    async def get(self, request):
        wdid = request.path_params['wikidataid']
        task = rels.instances.find_one({'WikiDataID': wdid})
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)
      
    async def put(self, request):
        pass
