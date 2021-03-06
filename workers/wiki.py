import asyncio
import pprint
import random
from datetime import datetime, timedelta
from urllib.parse import unquote

from bs4 import BeautifulSoup
from pymongo import MongoClient

from workers.web import get_html_async, get_text, get_text_async

client = MongoClient()

langs = ['en', 'sv', 'de', 'nl', 'fr', 'it', 'es', 'pt', 'ru', 'pl', 'uk', 'cs', 'ar',
         'he', 'zh', 'tr', 'az', 'vi', 'id', 'fi', 'hu', 'ja', 'fa', 'hi', 'bn', 'ko', 'el', 'th']


class Category(object):
    def __init__(self, lang, title) -> None:
        super().__init__()
        self.__lang = lang
        self.__title = title

    @property
    def lang(self):
        return self.__lang

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return 'https://{}.wikipedia.org/wiki/{}'.format(self.__lang, self.__title)

    async def parse(self):
        html, error = await get_html_async(self.url)


class Article(object):
    def __init__(self, lang, title) -> None:
        super().__init__()
        self.__lang = lang
        self.__title = title

    @property
    def lang(self):
        return self.__lang

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return 'https://{}.wikipedia.org/wiki/{}'.format(self.lang, self.title)

    async def categories(self):
        if not hasattr(self, '__categories'):
            await self.__parse()
        return self.__categories

    async def interwikis(self):
        if not hasattr(self, '__interwikis'):
            await self.__parse()
        return self.__interwikis

    async def __parse(self):
        html, error = await get_html_async(self.url)
        title_node = html.select_one('h1#firstHeading')
        if title_node:
            self.__title = title_node.text.strip()
        cat_nodes = html.select(
            '#catlinks div#mw-normal-catlinks ul li a[title]')
        if cat_nodes:
            self.__categories = []
            for cat_node in cat_nodes:
                self.__categories.append(
                    Category(self.lang, cat_node.get('title').strip()))
        nodes = html.select(
            'li.interlanguage-link a.interlanguage-link-target')
        if nodes:
            self.__interwikis = []
            for node in nodes:
                lang_title = unquote(node.get('href'))
                lang_title = lang_title[lang_title.find('/wiki/') + 6:]
                self.__interwikis.append(Article(node.get('lang'), lang_title))


def get_country_info(soup):
    countries = []
    nodes = soup.select("span[data-wikidata-property-id='P27'] a[title]")
    if nodes:
        for node in nodes:
            if 'Флаг' in node.get('title'):
                continue
            if node.get('title') in countries:
                continue
            countries.append(node.get('title'))
    return countries


def get_name_info(soup):
    name = None
    nodes = soup.select("div.ts_Спортсмен_имя div.label")
    if nodes:
        for node in nodes:
            name = node.text
    return name


def get_image_info(soup):
    name = None
    nodes = soup.select(
        "span[data-wikidata-property-id='P18'] a.image img[src]")
    if nodes:
        for node in nodes:
            name = 'https:{}'.format(node.get('src'))
    return name


def get_desc(soup):
    nodes = soup.select(
        "div#mw-content-text div.mw-parser-output > p")
    if nodes:
        return nodes[0].text


def get_bday_info(soup):
    name = None
    nodes = soup.select("span.bday")
    if nodes:
        for node in nodes:
            try:
                name = datetime.strptime(node.text, '%Y-%m-%d').date()
            except Exception as e:
                name = None
    return name


async def get_info(lang, title):
    print('INFO\tget_info({}, {})'.format(lang, title))
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text is None:
        return {'name': title, 'countries': []}
    category = {'name': title, 'countries': []}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        category['countries'] = get_country_info(soup)
        category['image'] = get_image_info(soup)
        category['desc'] = get_desc(soup)
        category['name'] = get_name_info(soup)
        if category['name'] is None:
            category['name'] = title
        category['bday'] = get_bday_info(soup)
    print('INFO\tget_info({}, {})\r\n\t{}'.format(lang, title, category))
    return category


async def get_externals(lang, title):
    print('--get_externals--{}--{}'.format(lang, title))
    wikis = {'lang': lang, 'name': title, 'externals': []}
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select('a.external.text')
        for node in nodes:
            if node.text == 'Facebook':
                wikis['externals'].append(node.get('href'))
            if node.text == 'Instagram':
                wikis['externals'].append(node.get('href'))
            if node.text == 'Твиттер':
                wikis['externals'].append(node.get('href'))
            if node.text == 'ВКонтакте':
                wikis['externals'].append(node.get('href'))
            if node.text == 'biathlon.com.ua':
                wikis['externals'].append(node.get('href'))
            if node.text == 'IBU':
                wikis['externals'].append(node.get('href'))
            print('\t--externals--{}'.format(wikis['externals']))
    await asyncio.sleep(10 + random.randint(4, 8))
    return wikis


async def process_seasons():
    seasons = client.ibustats.seasons.find({})
    wikis = [season for season in seasons]
    random.shuffle(wikis)
    for wiki in wikis:
        iws = await get_infobox('en', wiki['wiki']['en'])
        await asyncio.sleep(10 + random.randint(8, 16))
    for wiki in wikis:
        iws = await get_interwikis('en', wiki['wiki']['en'])
        await asyncio.sleep(10 + random.randint(8, 16))
        for iw in iws['interwikis'].keys():
            if iw in langs:
                client.ibustats.seasons.update_many({'wiki.en': wiki['wiki']['en']}, {
                    '$set': {'wiki.{}'.format(iw): iws['interwikis'][iw]}}, upsert=False)
    for wiki in wikis:
        client.ibustats.seasons.update_many({'wiki.en': wiki['wiki']['en']}, {
            '$unset': {'pvi_month': 1,
                       'lasttime': 1}}, upsert=False)
        for lang in wiki['wiki'].keys():
            pi = await get_pi(lang, wiki['wiki'][lang])
            client.ibustats.seasons.update_many({'wiki.{}'.format(lang): wiki['wiki'][lang]}, {
                '$set': {'pvi_month.{}'.format(lang): pi['pvi_month'],
                         'lasttime.{}'.format(lang): pi['lasttime']}}, upsert=False)
            await asyncio.sleep(10 + random.randint(8, 16))
    await asyncio.sleep(32)


async def get_infobox(lang, title):
    print('--get_infobox--{}--{}'.format(lang, title))
    wikis = {'lang': lang, 'name': title, 'infobox': {}}
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select(
            'li.interlanguage-link a.interlanguage-link-target')
        for _ in nodes:
            pass
    return wikis


async def process_countries():
    print('--process_countries--')
    countries = client.ibustats.countries.find({})
    wikis = [country for country in countries]
    random.shuffle(wikis)
    for wiki in wikis:
        iws = await get_interwikis('ru', wiki['wiki']['ru'])
        await asyncio.sleep(10 + random.randint(8, 16))
        for iw in iws['interwikis'].keys():
            if iw in ['en', 'de', 'fr']:
                client.ibustats.countries.update_many({'wiki.ru': wiki['wiki']['ru']}, {
                    '$set': {'wiki.{}'.format(iw): iws['interwikis'][iw]}}, upsert=False)
    for wiki in wikis:
        client.ibustats.countries.update_many({'wiki.ru': wiki['wiki']['ru']}, {
            '$unset': {'pvi_month': 1,
                       'lasttime': 1}}, upsert=False)
        for lang in wiki['wiki'].keys():
            pi = await get_pi(lang, wiki['wiki'][lang])
            client.ibustats.countries.update_many({'wiki.{}'.format(lang): wiki['wiki'][lang]}, {
                '$set': {'pvi_month.{}'.format(lang): pi['pvi_month'],
                         'lasttime.{}'.format(lang): pi['lasttime']}}, upsert=False)
            await asyncio.sleep(10 + random.randint(8, 16))
    for wiki in wikis:
        title = wiki['wiki']['ru']
        fi = await get_ci('ru', title)
        client.ibustats.countries.update_many({'wiki.ru': title}, {
            '$set': {'flag': fi['flag'], 'emblem': fi['emblem']}}, upsert=False)
        await asyncio.sleep(10 + random.randint(8, 16))


async def get_interwikis(lang, title):
    print('--get_interwikis--{}--{}'.format(lang, title))
    wikis = {'lang': lang, 'name': title, 'interwikis': {}}
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select(
            'li.interlanguage-link a.interlanguage-link-target')
        for node in nodes:
            lang_title = node.get('title')
            if '–' in lang_title:
                lang_title = lang_title[:lang_title.rfind('–')].strip()
            elif '—' in lang_title:
                lang_title = lang_title[:lang_title.rfind('—')].strip()
            wikis['interwikis'][node.get('lang')] = lang_title
            print('\t--interwiki--{}--{}'.format(node.get('lang'), lang_title))
    return wikis


async def get_pi(lang, title):
    print('--get_pi--{}--{}'.format(lang, title))
    text = get_text(
        'https://{}.wikipedia.org/w/index.php?title={}&action=info'.format(lang, title))
    if text is None:
        return {'name': title}
    category = {'name': title}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        category['pvi_month'] = get_pvi_month(soup)
        category['lasttime'] = get_lasttime(soup)
    return category


def get_pvi_month(soup):
    print('--get_pvi_month--')
    name = 0
    nodes = soup.select('div.mw-pvi-month')
    if nodes:
        for node in nodes:
            text = ''.join(node.text.split())
            text = ''.join(text.split(','))
            text = ''.join(text.split('.'))
            try:
                name = int(text)
            except:
                name = 0
            print('get_pvi_month - [{}] - {}'.format(node.text, name))
    return name


def get_lasttime(soup):
    print('--get_lasttime--')
    name = None
    nodes = soup.select('tr#mw-pageinfo-lasttime td a')
    if nodes:
        for node in nodes:
            name = node.text.strip()
            print('get_lasttime - {}'.format(name))
    return name


async def get_ci(lang, title):
    print('--get_ci--{}--{}'.format(lang, title))
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text is None:
        return {'name': title}
    info = {'name': title}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        info['flag'] = get_flag_info(soup)
        info['emblem'] = get_emblem_info(soup)
    print('INFO\tget_ci({}, {})\r\n\t{}'.format(lang, title, info))
    return info


def get_flag_info(soup):
    print('--get_flag_info--')
    name = None
    nodes = soup.select(
        'span[data-wikidata-property-id="P41"] a.image img[src]')
    if nodes:
        for node in nodes:
            name = 'https:{}'.format(node.get('src').replace(
                '{}px'.format(node.get('width')), '1024px'))
            print('get_flag_info - {}'.format(name))
    return name


def get_emblem_info(soup):
    print('--get_emblem_info--')
    name = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Herb_%C5%81ab%C4%99d%C5%BA_1.svg/1024px-Herb_%C5%81ab%C4%99d%C5%BA_1.svg.png'
    nodes = soup.select(
        'span[data-wikidata-property-id="P94"] a.image img[src]')
    if nodes:
        for node in nodes:
            name = 'https:{}'.format(node.get('src').replace(
                '{}px'.format(node.get('width')), '1024px'))
            print('get_emblem_info - {}'.format(name))
    return name


async def get_links(lang, title):
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text is None:
        return {'title': title, 'links': []}
    category = {'title': title, 'links': []}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        cat_nodes = soup.select('div#mw-content-text a[title]')
        if cat_nodes:
            for cat_node in cat_nodes:
                category['links'].append(cat_node.get('title'))
    return category


async def get_pages(lang, title):
    url = 'https://{}.wikipedia.org/wiki/{}'.format(lang, title)
    pages = []
    while url is not None:
        ps = await _get_pages(url)
        for p in ps['pages']:
            pages.append(p)
        url = 'https://ru.wikipedia.org{}'.format(
            ps['next']) if ps['next'] else None
    return pages


async def _get_pages(url):
    text = get_text(url)
    await asyncio.sleep(4)
    if text is None:
        return {'pages': [], 'next': None}
    category = {'pages': [], 'next': None}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        next_nodes = soup.select('div#mw-pages a[title]')
        if next_nodes:
            for next_node in next_nodes:
                if 'Следующая страница' in next_node.text:
                    category['next'] = next_node.get('href')
        cat_nodes = soup.select('div#mw-pages div.mw-category li a[title]')
        if cat_nodes:
            for cat_node in cat_nodes:
                category['pages'].append(cat_node.get('title'))
    return category
