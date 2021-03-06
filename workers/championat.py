import asyncio
import random
from datetime import datetime

from bs4 import BeautifulSoup
from pymongo import MongoClient

from workers.web import get_text

client = MongoClient()


class Champ(object):
    def __init__(self):
        pass


async def process_players():
    racers = client.ibustats.racers.find({})
    wikis = []
    for racer in racers:
        if 'Редактировать' in racer['wiki']['ru']:
            client.ibustats.racers.remove({'wiki.ru': racer['wiki']['ru']})
            continue
        if 'champ' in racer:
            wikis.append(racer)
    random.shuffle(wikis)
    for wiki in wikis:
        await process_player(wiki)
        await asyncio.sleep(16 + random.randint(4, 12))
    await asyncio.sleep(32)


async def process_player(player):
    client.ibustats.racers.update_one({'champ.cc_id': player['champ']['cc_id']}, {
        '$set': {'images': []}}, upsert=False)
    text2 = get_text(
        'https://www.championat.com/biathlon/_biathlonworldcup/tournament/{}/players/{}/'
        .format(player['champ']['tournaments'][0], player['champ']['cc_id']))
    if text2:
        soup = BeautifulSoup(text2, 'html.parser')
        images = soup.select(
            'div._player div.entity-header__info div.entity-header__img img')
        for image in images:
            update_image(player, image)
        nodes = soup.select('div._player.entity-header > div > ul > li')
        for node in nodes:
            if 'Команда:' in node.text:
                update_team(player, node)
            if 'Дата рождения:' in node.text:
                update_bday(player, node)
    await asyncio.sleep(16 + random.randint(8, 16))


def update_image(player, node):
    if node:
        img = node.get('src')
        print(
            '{} - {} - {}'.format(player['champ']['cc_id'], player['name'], img))
        client.ibustats.racers.update_one({'champ.cc_id': player['champ']['cc_id']}, {
            '$addToSet': {'images': img}}, upsert=False)


def update_bday(player, node):
    team = node.text.split(':')[-1].strip()
    bday = datetime.now().date()
    if team:
        try:
            bday = datetime.strptime(team, '%d.%m.%Y').date()
        except Exception as e:
            bday = datetime.now().date()
        print(
            '{} - {} - {}'.format(player['champ']['cc_id'], player['name'], str(bday)))
        client.ibustats.racers.update_one({'champ.cc_id': player['champ']['cc_id']}, {
            '$set': {'bday': str(bday)}}, upsert=False)


def update_team(player, node):
    team = node.text.split(':')[-1].strip()
    if team:
        print(
            '{} - {} - {}'.format(player['champ']['cc_id'], player['name'], team))
        client.ibustats.racers.update_one({'champ.cc_id': player['champ']['cc_id']}, {
            '$addToSet': {'countries': team}}, upsert=False)
        client.ibustats.countries.update_one({'wiki.ru': team}, {
            '$set': {'last_modified': datetime.now()}}, upsert=True)


async def process_season(season):
    text2 = get_text(
        'https://www.championat.com/biathlon/_biathlonworldcup/tournament/{}/players/'.format(season['cc_id']))
    if text2:
        soup = BeautifulSoup(text2, 'html.parser')
        nodes = soup.select('a[href]')
        for node in nodes:
            if '/biathlon/_biathlonworldcup/' in node.get(
                'href'
            ) and '/players/' in node.get('href'):
                player = get_player(node)
                client.ibustats.racers.update_one({'wiki.ru': player['name']}, {
                    '$set': {'champ.cc_id': player['cc_id']}}, upsert=True)
                client.ibustats.racers.update_one({'wiki.ru': player['name']}, {
                    '$addToSet': {'champ.tournaments': player['tournament']}}, upsert=False)
    await asyncio.sleep(4 + random.randint(4, 12))
    text = get_text(
        'https://www.championat.com/biathlon/_biathlonworldcup/tournament/{}/teams/'.format(season['cc_id']))
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select('a[href]')
        for node in nodes:
            if '/biathlon/_biathlonworldcup/' in node.get(
                'href'
            ) and '/teams/' in node.get('href'):
                country = get_country(node)


def get_country(node):
    country = {}
    prev = ''
    parts = node.get('href').split('/')
    for part in parts:
        if prev == 'teams':
            country['cc_id'] = part
            country['name'] = node.text.strip()
        elif prev == 'tournament':
            country['tournament'] = part
        prev = part
    return country


def get_player(node):
    player = {}
    prev = ''
    parts = node.get('href').split('/')
    for part in parts:
        if prev == 'players':
            player['cc_id'] = part
            player['name'] = node.text.strip()
            print('player: {}'.format(player['name']))
        elif prev == 'tournament':
            player['tournament'] = part
        prev = part
    return player


async def process_seasons():
    seasons = client.ibustats.seasons.find({})
    for season in seasons:
        await process_season(season)
        await asyncio.sleep(4 + random.randint(4, 12))


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
