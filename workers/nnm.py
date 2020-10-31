import requests
from bs4 import BeautifulSoup

r = requests.get('http://nnmclub.to/forum/portal.php?c=12&sid=3c44b5b5baf94f59642bd0a373db4884')
soup = BeautifulSoup(r.text, features='html.parser')
n=1
for t in soup.select('table.pline'):
    for link in t.select('a[href]'):
        if link['href'].startswith('magnet'):
            pcatHead = t.select_one('td.pcatHead')
            print(n, pcatHead.text)
            print('\t', link['href'])
            print('\t', pcatHead.text.split('-')[0].strip())
            print('\t', pcatHead.text.split('-')[1].split('(')[0].strip())
            n=n+1
