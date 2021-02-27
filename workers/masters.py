#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import requests
from bs4 import BeautifulSoup


def wiki(page):
    print(page)
    time.sleep(4)
    url = 'https://en.wikipedia.org' + page
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features='html.parser')
    for link in soup.select('#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr:nth-child(2)'):
        print('\t', link.text, '\n\r')
    for link in soup.select('#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr'):
        for scope in link.select('th'):
            if scope.text == 'Champion':
                c = link.select_one('td > a')
                print('\tChampion', c['title'], '\n\r')
            if scope.text == 'Runner-up':
                rup = link.select_one('td > a')
                print('\tRunner-up', rup['title'], '\n\r')


r = requests.get(
    'https://en.wikipedia.org/wiki/Tennis_Masters_Series_records_and_statistics')
soup = BeautifulSoup(r.text, features='html.parser')
for link in soup.select('a[href]'):
    if '*' in link.text:
        print(link.text, link['href'])
        wiki(link['href'])
