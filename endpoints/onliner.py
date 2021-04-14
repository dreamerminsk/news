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










class OnlinerView(HTTPEndpoint):
    async def get(self, request):
        return templates.TemplateResponse('/onliner/OnlinerView.html', {'request': request})
