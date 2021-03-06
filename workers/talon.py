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

ws = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ru.wikipedia/all-access/user/Слон/daily/2020070100/2021020723'


class Policlinic(object):
    def __init__(self, title, url) -> None:
        super().__init__()
        self.__title = title
        self.__url = url

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url


class Talon(object):
    def __init__(self) -> None:
        super().__init__()

    @property
    def url(self):
        return 'https://talon.by/policlinics'

    async def policlinics(self):
        if not hasattr(self, '__policlinics'):
            await self.__parse()
        return self.__policlinics

    async def __parse(self):
        html, error = await get_html_async(self.url)
        pol_nodes = html.select('div.policlinic h5 a')
        if pol_nodes:
            self.__policlinics = []
            for pol_node in pol_nodes:
                self.__policlinics.append(Policlinic(
                    pol_node.text, pol_node.get('href')))


async def process_policlinics():
    print('--process_policlinics--')
    talon = Talon()
    ps = await talon.policlinics()
    for p in ps:
        print('\t--process_policlinics--\r\n\t{}\r\n\t{}'.format(p.title, p.url))
