import asyncio
import pprint
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo import MongoClient
from starlette.endpoints import HTTPEndpoint
from starlette.responses import (JSONResponse, PlainTextResponse,
                                 RedirectResponse)
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

client = MongoClient()
ibustats = client.ibustats


class RacersEndpoint(HTTPEndpoint):
    async def get(self, request):
        racers = ibustats.racers.find({})
        latest = []
        for racer in racers:
            racer['_id'] = str(racer['_id'])
            if 'bday' in racer:
                racer['bday'] = str(racer['bday'])
            if 'last_modified' in racer:
                racer['last_modified'] = str(racer['last_modified'])
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


class NamesEndpoint(HTTPEndpoint):
    async def get(self, request):
        startswith = request.path_params['startswith']
        racers = ibustats.racers.find(
            {'wiki.ru': {'$regex': '^{}'.format(startswith)}})
        latest = []
        for racer in racers:
            racer['_id'] = str(racer['_id'])
            if 'bday' in racer:
                racer['bday'] = str(racer['bday'])
            if 'last_modified' in racer:
                racer['last_modified'] = str(racer['last_modified'])
            latest.append(racer)
        return JSONResponse({'status': 'ok', 'racers': latest})

    async def post(self, request):
        pass


class YearMonthEndpoint(HTTPEndpoint):
    async def get(self, request):
        pass

class BirthdatesEndpoint(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse('Birthdates.html', {'request': request})
