#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time



def wiki2(page):
    print(page)
    time.sleep(4)
    url = 'https://en.wikipedia.org' + page
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features='html.parser')
    for link in soup.select('#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr:nth-child(2)'):
        print ('\t', link.text, '\n\r')
    for link in soup.select('#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr'):
        for scope in link.select('th'):
            if scope.text == 'Champion':
                c = link.select_one('td > a')
                print ('\tChampion', c['title'], '\n\r')
            if scope.text == 'Runner-up':
                rup = link.select_one('td > a')
                print ('\tRunner-up', rup['title'], '\n\r')


def wiki(page):
    print(page)
    time.sleep(4)
    url = 'https://en.wikipedia.org/wiki/' + page
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features='html.parser')
    k = 1
    for link in soup.select('span.mw-headline'):
        print ('{}. {} - {}'.format(k, link.parent.name, link.text))
        if 'table' in link.parent.find_next_siblings()[0].name:
            table = link.parent.findNext('table')
            row = table.find('tr')
            for td in row.findChildren('td'):
                if len(td.text):
                    print ('\t"{}"'.format(td.text.strip()))
        k += 1


wiki('2019 St. Petersburg Open – Singles')
