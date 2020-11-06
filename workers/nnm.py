#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

r = requests.get('http://nnmclub.to/forum/portal.php?c=12')
soup = BeautifulSoup(r.text, features='html.parser')
n = 1
for t in soup.select('table.pline'):
    for link in t.select('a[href]'):
        if link['href'].startswith('magnet'):
            pcatHead = t.select_one('td.pcatHead a.pgenmed')
            print ('')
            print (n, pcatHead['title'])
            print ('\tTOPIC\t', pcatHead['href'][16:])
            print ('\tHASH\t', link['href'][20:])
            if ' - ' in pcatHead['title']:
                ad = pcatHead['title'].find(' - ')
                td = pcatHead['title'].find(' (', ad)
                td = (td if td > -1 else pcatHead['title'].find(' [', ad))
                print ('\tARTIST\t', (pcatHead['title'])[0:ad].strip())
                print ('\tTITLE\t', (pcatHead['title'])[ad + 3:td].strip())
                gs = (pcatHead['title'])[pcatHead.text.find('<')
                    + 1:pcatHead['title'].find('>')].strip()
                print ('\tGENRES\t', gs.strip())
            n = n + 1
