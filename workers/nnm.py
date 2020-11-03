import requests
from bs4 import BeautifulSoup

r = requests.get('http://nnmclub.to/forum/portal.php?c=12&sid=3c44b5b5baf94f59642bd0a373db4884')
soup = BeautifulSoup(r.text, features='html.parser')
n=1
for t in soup.select('table.pline'):
    for link in t.select('a[href]'):
        if link['href'].startswith('magnet'):
            pcatHead = t.select_one('td.pcatHead a.pgenmed')
            print(n, pcatHead['title'])
            print('\t', link['href'])
            if ' - ' in pcatHead['title']:
                ad = pcatHead['title'].find(' - ')
                td = pcatHead['title'].find(' (', ad)
                td = td if td > -1 else pcatHead['title'].find(' [', ad)
                print('\t', pcatHead['title'][0 : ad].strip())
                print('\t', pcatHead['title'][ad + 3 : td].strip())
                gs = pcatHead['title'][pcatHead.text.find('<')+1 : pcatHead['title'].find('>')].strip()
                print('\t', gs.strip())
            n=n+1
            
