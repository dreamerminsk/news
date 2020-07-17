import requests

r = requests.get('https://news.tut.by/rss/all.rss')
print(r.text)
