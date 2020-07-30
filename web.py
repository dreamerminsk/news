import requests

from fake_useragent import UserAgent


def get_text(url):
    try:
        r = requests.get(url, headers={'User-Agent': UserAgent().random})
        return r.text
    except Exception as e:
        print('ERROR: {}'.format(e))
        return None
