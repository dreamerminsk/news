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
