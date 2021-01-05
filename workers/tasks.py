async def queue_ibu2():
    await asyncio.sleep(4)
    total = 0
    links = await get_pages('ru', 'Категория:Биатлонисты по алфавиту')
    for link in links:
        found = client.ibustats.racers.find_one(
            {'wiki.ru': link})
        if found is None:
            total += 1
            client.ibustats.racers.insert_one(
                {'wiki': {'ru': link}})
    print('queue_ibu2(): {}'.format(total))
    await asyncio.sleep(32)


async def queue_ibu():
    await asyncio.sleep(4)
    total = 0
    links = await get_links('ru', 'Призёры чемпионатов мира по биатлону (мужчины)')
    for link in links['links']:
        if ', ' not in link:
            continue
        found = client.ibustats.racers.find_one(
            {'wiki.ru': link})
        if found is None:
            total += 1
            client.ibustats.racers.insert_one(
                {'wiki': {'ru': link}})
    print('queue_ibu(): {}'.format(total))
    await asyncio.sleep(32)
