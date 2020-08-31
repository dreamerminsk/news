from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient

from web import get_text

client = MongoClient()


async def get_category(title):
    while True:
        print('\r\n{}'.format(title))
        text = get_text(
            'https://en.wikipedia.org/wiki/{}'.format(title))
        if text:
            soup = BeautifulSoup(text, 'html.parser')
            wdi_nodes = soup.select('li#t-wikibase a[href]')
            if wdi_nodes:
                for wdi_node in wdi_nodes:
                    wdi = wdi_node.get('href').split('/')[-1]
                    print('\tWikiDataID: {} - {}'.format(wdi, type(wdi)))
                    us = client.rels.categories.update_one(
                        {'labels.en': title}, {'$set': {'wikidataid': wdi}})
                    print('\t{} - {}'.format(us.matched_count, us.modified_count))
            cat_nodes = soup.select('div#mw-normal-catlinks ul li a[title]')
            if cat_nodes:
                client.rels.categories.update_one(
                    {'labels.en': title},
                    {'$set': {'categories': []}})
                for cat_node in cat_nodes:
                    cat_title = cat_node.get('title')
                    print('\t{}'.format(cat_title))
                    client.rels.categories.update_one(
                        {'labels.en': title},
                        {'$push': {'categories': cat_title}})
                    found = client.rels.categories.find_one(
                        {'labels.en': cat_title})
                    if found is None:
                        client.rels.categories.insert_one(
                            {'labels': {'en': cat_title}})
