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
        latest = [db for db in dbs]
        return JSONResponse({'status': 'ok', 'dbs': latest})


class DbEndpoint(HTTPEndpoint):
    async def get(self, request):
        db = request.path_params['db']
        try:
            stats = client[db].command({'dbstats': 1})
            return JSONResponse({'status': 'ok', 'dbstats': stats})
        except Exception as e:
            return JSONResponse({'status': 'error', 'exception': str(e)})


class CollsEndpoint(HTTPEndpoint):
    async def get(self, request):
        db = request.path_params['db']
        lcn = client[db].list_collection_names()
        colls = [cn for cn in lcn]
        return JSONResponse({'status': 'ok', 'colls': colls})



class CollEndpoint(HTTPEndpoint):
    async def get(self, request):
        db = request.path_params['db']
        coll = request.path_params['coll']
        try:
            stats = client[db].command({'collstats': 1})
            return JSONResponse({'status': 'ok', 'collstats': stats})
        except Exception as e:
            return JSONResponse({'status': 'error', 'exception': str(e)})




class AdminView(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse('/admin/AdminView.html', {'request': request})
