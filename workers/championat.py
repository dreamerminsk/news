import asyncio
import pprint
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient

from workers.web import get_text

client = MongoClient()


async def process_season(season):
    text2 = get_text(
        'https://www.championat.com/biathlon/_biathlonworldcup/tournament/{}/players/'.format(season['cc_id']))
    if text2:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select('a[href]')
        for node in nodes:
            if '/biathlon/_biathlonworldcup/' in url:
                if '/players/' in url:
                    player = get_player(node)
                    client.ibustats.racers.update_one({'wiki.ru': player['name']}, {
                        '$set': {'champ.cc_id': player['cc_id']}}, upsert=True)
    text = get_text(
        'https://www.championat.com/biathlon/_biathlonworldcup/tournament/{}/teams/'.format(season['cc_id']))
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select('a[href]')
        for node in nodes:
            if '/biathlon/_biathlonworldcup/' in url:
                if '/teams/' in url:
                    country = get_country(node)



def get_country(node):
    country = {}
    prev = ''
    parts = node.get('href').split('/')
    for part in parts:
        if prev == 'tournament':
            country['tournament'] = part
        if prev == 'teams':
            country['cc_id'] = part
            country['name'] = node.text
        prev = part
    return country

def get_player(node):
    player = {}
    prev = ''
    parts = node.get('href').split('/')
    for part in parts:
        if prev == 'tournament':
            player['tournament'] = part
        if prev == 'players':
            player['cc_id'] = part
            player['name'] = node.text
        prev = part
    return player


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
