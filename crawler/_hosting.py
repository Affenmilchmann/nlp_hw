import requests
import random
import re
from time import sleep
from typing import List, Tuple
from pprint import pprint
from bs4 import BeautifulSoup

from ._conf import MAIN_URL, DOMAIN, query_template

def __parse_page(url: str) -> BeautifulSoup:
    """Loads html from given `url` and feeds it to bs4

    Args:
        url (str)

    Returns:
        BeautifulSoup: BeautifulSoup parsed odject
    """
    raw_html = requests.get(url).text
    return BeautifulSoup(raw_html, features='html.parser')

def get_hosts(max_n: int = 10) -> List[str]:
    """Gets up to `max_n` random links to individual rated hosts from https://hosting101.ru/rating-popular.html

    Args:
        max_n (int, optional): Max host links count. Defaults to 10.

    Returns:
        list[str]: list of links to rated hosts. Example: https://hosting101.ru/reg.ru
    """
    bs = __parse_page(MAIN_URL)
    table = bs.find('div', class_='providers-rating-2')
    urls = [ x.get('href') for x in table.find_all('a') ]
    urls = filter(lambda x: not re.match(r'^/uptime/.*', x), urls)
    return [ DOMAIN + x for x in random.sample(list(urls), max_n) ]

def parse_host(url: str, positive: bool, max_n: int = None, delay: Tuple[int, int] = None) -> List[str]:
    """Parse host's reviews

    Args:
        url (str): link to host reviews page
        positive (bool): parse positive or negative filtered
        max_n (int, optional): Max reviews. None means no limit (up to 20). Defaults to None.
        delay (Tuple[int, int]): do a random delay in `delay` interval.

    Returns:
        list[str]: List of review texts.
    """
    mode = 'positive' if positive else 'negative'
    bs = __parse_page(url + query_template.format(mode=mode))
    comment_blocks = bs.find_all('div', class_=f'comment-{mode}', limit=max_n)
    content_blocks = [ x.find('div', class_='content') for x in comment_blocks ]
    comments = [ x.find('p').text for x in content_blocks ]
    if delay: sleep(delay[0] + random.random() * (delay[1] - delay[0]))
    return comments
