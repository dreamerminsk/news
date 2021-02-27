#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import pprint
import random
import time
from datetime import datetime, timedelta
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from workers.web import get_html_async, get_text, get_text_async

talon = 'https://talon.by/'

p = 'https://talon.by/policlinic/minsk-1dp/order'
d = 'https://talon.by/policlinic/minsk-1dp/order/1943'
t = 'https://talon.by/policlinic/minsk-1dp/order/1943/3473'

dd = 'https://talon.by/policlinic/minsk-1dp/doctors/16484'
ddt = 'https://talon.by/policlinic/minsk-1dp/order/1944/3483'
ddtt = 'https://talon.by/policlinic/minsk-1dp/order/1944/3483/2125898'


policlinics = 'https://talon.by/policlinics'


class Talon(object):
    def __init__(self) -> None:
        super().__init__()

    @property
    def url(self):
        return 'https://talon.by/policlinics'

    async def __parse(self):
        html, error = await get_html_async(self.url)
        title_node = html.select_one('h1#firstHeading')
        if title_node:
            self.__title = title_node.text.strip()


async def process_policlinics():
    print('--process_policlinics--')
