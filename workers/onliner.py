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

onliner = 'https://onliner.by/'

class Article(object):
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
    
    
def get_articles(url):
    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url))
    html, error = get_text(url)
    pol_nodes = html.select('a[href]')
    urls = set()
    if pol_nodes:
        for pol_node in pol_nodes:
            ref = pol_node.get('href')
            if '#comments' in ref:
                continue
            if '/2021/' in ref or '/2020/' in ref:
                if 'https://' in ref:
                    urls.add(ref)
                else:
                    urls.add('{}{}'.format(base_url, ref))
    return urls


class Onliner(object):
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


async def process_articles():
    print('--process_articles--')
    onliner = Onliner()
    ps = await onliner.policlinics()
    for p in ps:
        print('\t--process_policlinics--\r\n\t{}\r\n\t{}'.format(p.title, p.url))
