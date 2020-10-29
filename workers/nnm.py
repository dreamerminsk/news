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
            n=n+1