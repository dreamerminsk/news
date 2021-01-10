from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from workers.web import get_text

import asyncio
import pprint
from datetime import datetime, timedelta

from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()


async def process_season(season):
    text = get_text('https://www.championat.com/biathlon/_biathlonworldcup/tournament/{}/teams/'.format(season['cc_id']))
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select('a[href]')
        for node in nodes:
            url = node.get('href')
            if '' not in url:
                continue
            if '' not in url:
                continue


async def process_seasons():
    seasons = client.ibustats.seasons.find({})
    for season in seasons:
        await process_season(season)


async def process_tournaments():
    client.ibustats.seasons.update_one({'cc_id': 597}, {
        '$set': {'title': '2020/2021'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 551}, {
        '$set': {'title': '2019/2020'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 497}, {
        '$set': {'title': '2018/2019'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 450}, {
        '$set': {'title': '2017/2018'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 402}, {
        '$set': {'title': '2016/2017'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 334}, {
        '$set': {'title': '2015/2016'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 283}, {
        '$set': {'title': '2014/2015'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 172}, {
        '$set': {'title': '2013/2014'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 83}, {
        '$set': {'title': '2012/2013'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 55}, {
        '$set': {'title': '2011/2012'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 34}, {
        '$set': {'title': '2010/2011'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 15}, {
        '$set': {'title': '2009/2010'}}, upsert=True)
    client.ibustats.seasons.update_one({'cc_id': 2}, {
        '$set': {'title': '2008/2009'}}, upsert=True)
