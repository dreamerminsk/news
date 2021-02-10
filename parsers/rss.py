import asyncio
import xml.etree.ElementTree as etree
from datetime import datetime, timedelta

from bs4 import BeautifulSoup



async def start_job():
    count = articles.count_documents({})
    print('{}. {}'.format(datetime.now(), count))
    news.tasks.update_one({'name': 'feeds'}, {
        '$set': {'start': datetime.now(), 'feeds': 0, 'articles': count}}, upsert=True)
    feeds.update_one({'link': 'https://dev.by/rss'}, {
        '$set': {'last_access': datetime.now(), 'next_access': datetime.now(), 'ttl': 1000}}, upsert=True)
    q = asyncio.Queue()
    loop = asyncio.get_event_loop()
    tasks = [#loop.create_task(queue_feeds(q)),
             #loop.create_task(process_feeds(q)),
            loop.create_task(process_countries()),
            loop.create_task(queue_wiki_info()),
            loop.create_task(process_players()),
            loop.create_task(process_seasons())]



async def parse(text):
    soup = BeautifulSoup(text, 'xml')
    channel = {}
    for channel_node in soup.find_all('channel'):
        channel = await parse_channel(channel_node)
    return channel


async def parse_channel(node):
    channel = {}
    channel['title'] = node.find('title').text
    channel['link'] = node.find('link').text
    channel['description'] = node.find('description').text
    channel['items'] = []
    for item_node in node.find_all('item'):
        channel['items'].append(await parse_item(item_node))
    return channel


async def parse_item(item):
    article = {}
    article['title'] = item.find('title').text
    article['link'] = item.find('link').text
    if '?' in article['link']:
        article['link'] = article['link'][:article['link'].find('?')]
    article['last_access'] = datetime.now()
    return article




async def queue_feeds(q):
    while True:
        for feed in feeds.find({"next_access": {"$lte": datetime.now()}}):
            await q.put(feed)
        await asyncio.sleep(60)


async def process_feeds(q):
    while True:
        try:
            feed = await q.get()
            await update_feed(feed)
        finally:
            q.task_done()
            news.tasks.update_one({'name': 'feeds'}, {
                '$inc': {'feeds': 1}}, upsert=True)


async def update_feed(feed):
    i = 0
    text = get_text(feed['link'])
    if text:
        try:
            soup = BeautifulSoup(text, 'lxml-xml')
            channel = await get_channel(soup)
            feeds.update_one({'_id': feed['_id']}, {
                '$set': {
                    'title': channel['title'],
                    'description': channel['description'],
                    'image': channel.get('image', ''),
                    'exception': None}},
                upsert=False)
            for channel_node in soup.find_all('channel'):
                for item in channel_node.find_all('item'):
                    title = item.find('title').text
                    link = item.find('link').text
                    if '?' in link:
                        link = link[:link.find('?')]
                    if not articles.find_one({"link": link}):
                        i += 1
                        articles.insert_one({"link": link, "title": title})
        except Exception as e:
            feeds.update_one({'_id': feed['_id']}, {
                '$set': {'exception': getattr(e, 'message', str(e))}},
                upsert=False)

        feeds.update_one({'_id': feed['_id']}, {
                         '$set': {'last_access': datetime.now()}}, upsert=False)
        if i > 0:
            feeds.update_one({'_id': feed['_id']}, {
                '$set': {'ttl': 0.9 * feed['ttl']}}, upsert=False)
            feeds.update_one({'_id': feed['_id']}, {
                '$set': {'next_access': datetime.now() + timedelta(seconds=0.9 * feed['ttl'])
                         }}, upsert=False)
        else:
            feeds.update_one({'_id': feed['_id']}, {
                '$set': {'ttl': 1.1 * feed['ttl']}}, upsert=False)
            feeds.update_one({'_id': feed['_id']}, {
                '$set': {'next_access': datetime.now() + timedelta(seconds=1.1 * feed['ttl'])
                         }}, upsert=False)


async def get_channel(soup):
    channel = {}
    for node in soup.find_all('channel'):
        for child in node.children:
            if child.name == 'title':
                channel['title'] = child.text
            if child.name == 'description':
                channel['description'] = child.text
            if child.name == 'image':
                for image in child.children:
                    if image.name == 'url':
                        channel['image'] = image.text
    return channel

