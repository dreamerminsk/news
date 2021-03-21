
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time


def get_text(url):
    try:
        r = requests.get(url, headers={'User-Agent': UserAgent().random})
        html = BeautifulSoup(r.text, 'html.parser')
        return (html, None)
    except Exception as e:
        print('ERROR: {}\r\n{}'.format(url, e))
        return (None, e)
        
        
title_selector = 'div.news-header__title' 
views_selector = 'div.news-header__button_views'  
comments_selector = '#news-header-comments-counter' 
time_selector = 'div.news-header__time'  
author_selector = 'div.news-header__author'  

def get_article(url):
    html, error = get_text(url)
    title_nodes = html.select(title_selector)
    if title_nodes:
        print(title_nodes[0].text.strip())
    views_nodes = html.select(views_selector)
    if views_nodes:
        print(views_nodes[0].text.strip())
    comments_nodes = html.select(comments_selector)
    if comments_nodes:
        print(comments_nodes[0].text.strip())
        
    time_nodes = html.select(time_selector)
    if time_nodes:
        print(time_nodes[0].text.strip())
    author_nodes = html.select(author_selector)
    if author_nodes:
        print(author_nodes[0].text.strip())
        
html, error = get_text('https://onliner.by/')
pol_nodes = html.select('a[href]')
if pol_nodes:
    cs = []
    for pol_node in pol_nodes:
        if '#comments' in pol_node.get('href'):
            continue
        if '/2021/' in pol_node.get('href'):
            time.sleep(4)
            get_article(pol_node.get('href'))
            time.sleep(30)