from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from workers.web import get_text


async def get_category(title):
    text = get_text('https://en.wikipedia.org/wiki/{}'.format(title))
    if text is None:
        return {'wikidataid': None, 'categories': []}
    category = {'wikidataid': 'None', 'categories': []}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        wdi_node = soup.select_one('li#t-wikibase a[href]')
        if wdi_node:
            category['wikidataid'] = wdi_node.get('href').split('/')[-1]
        cat_nodes = soup.select('div#mw-normal-catlinks ul li a[title]')
        if cat_nodes:
            for cat_node in cat_nodes:
                category['categories'].append(cat_node.get('title'))
    return category




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
    print('INFO\tget_info({}, {}'.format(lang, title))
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text is None:
        return {'name': title, 'countries': []}
    category = {'name': title, 'countries': []}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        category['countries'] = get_country_info(soup)
        category['name'] = get_name_info(soup)
        if category['name'] == None:
            category['name'] = title
        category['bday'] = get_bday_info(soup)
    print('INFO\tget_info({}, {})\r\n\t{}'.format(lang, title, category))
    return category



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
        if ps['next']:
            url = 'https://ru.wikipedia.org{}'.format(ps['next'])
        else:
            url = None
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


