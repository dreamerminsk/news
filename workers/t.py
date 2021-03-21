
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
    print('---------------------------------')
    print(url)
    html, error = get_text(url)
    title_nodes = html.select(title_selector)
    if title_nodes:
        print(title_nodes[0].text.strip())
    views_nodes = html.select(views_selector)
    if views_nodes:
        views = int(''.join(views_nodes[0].text.split()))
        print('\tviews: {}'.format(views))
    comments_nodes = html.select(comments_selector)
    if comments_nodes:
        comments = int(''.join(comments_nodes[0].text.split()))
        print('\tcomments: {}'.format(comments))        
    time_nodes = html.select(time_selector)
    if time_nodes:
        print(time_nodes[0].text.strip())
    author_nodes = html.select(author_selector)
    if author_nodes:
        print(author_nodes[0].text.strip())
        

def get_articles(url):
    html, error = get_text(url)
    pol_nodes = html.select('a[href]')
    urls = set()
    if pol_nodes:
        for pol_node in pol_nodes:
            if '#comments' in pol_node.get('href'):
                continue
            if '/2021/' in pol_node.get('href'):
                if 'https://' in pol_node.get('href'):
                    urls.add(pol_node.get('href'))
                else:
                    urls.add('{}{}'.format(url, pol_node.get('href')))
    return urls

topics = ['https://auto.onliner.by', 'https://people.onliner.by', 'https://realt.onliner.by', 'https://tech.onliner.by']
for topic in topics:  
    urls = get_articles(topic)              
    for url in urls:
        time.sleep(4)
        get_article(url)
        time.sleep(30)