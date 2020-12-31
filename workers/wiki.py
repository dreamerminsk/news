from bs4 import BeautifulSoup

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



async def get_info(lang, title):
    text = get_text('https://{}.wikipedia.org/wiki/{}'.format(lang, title))
    if text is None:
        return {'name': title, 'countries': []}
    category = {'name': title, 'countries': []}
    if text:
        soup = BeautifulSoup(text, 'html.parser')
        nodes = soup.select("span[data-wikidata-property-id='P27'] a[title]")
        if nodes:
            for node in nodes:
                category['countries'].append(node.get('title'))
        nodes = soup.select("div.ts_Спортсмен_имя div.label")
        if nodes:
            for node in nodes:
                category['name'] = node.text
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
