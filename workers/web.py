import requests
import httpx

from fake_useragent import UserAgent


def get_text(url):
    try:
        r = requests.get(url, headers={'User-Agent': UserAgent().random})
        return r.text
    except Exception as e:
        print('ERROR: {}\r\n{}'.format(url, e))
        return None
