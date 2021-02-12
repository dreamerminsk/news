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


class DbsEndpoint(HTTPEndpoint):
    async def get(self, request):
        dbs = client.list_databases()
        latest = []
        for db in dbs:
            latest.append(db)
        return JSONResponse({'status': 'ok', 'racers': latest})


class DbEndpoint(HTTPEndpoint):
    async def get(self, request):
        name = request.path_params['name']
        task = ibustats.countries.find_one({'WikiDataID': wdid})
        if task is not None:
            task['_id'] = str(task['_id'])
        else:
            task = {
            }
        return JSONResponse(task)


class AdminView(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse('/admin/AdminView.html', {'request': request})
