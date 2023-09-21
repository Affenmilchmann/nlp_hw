import requests
import random
import re
from tqdm import tqdm
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
    try:
        raw_html = requests.get(url).text
    except Exception as e:
        print(f"Sleeping for 60 sec...\nConnection exception: {e}")
        sleep(60)
        try:
            raw_html = requests.get(url).text
        except Exception:
            return None
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
    urls = [ x for x in urls if not re.match(r'^/uptime/.*', x) ]
    return [ DOMAIN + x for x in random.sample(list(urls), min(max_n, len(urls))) ]

def parse_host(url: str, positive: bool = None, delay: Tuple[int, int] = None, max_pages: int = None, pb: tqdm = None) -> List[str]:
    """Parse host's reviews

    Args:
        url (str): link to host reviews page
        positive (bool): parse positive or negative filtered
        delay (Tuple[int, int]): do a random delay in `delay` interval.
        max_pages (int): maximum amount af pages to parse (one page contains un to 20 reviews)

    Returns:
        list[str]: List of review texts.
    """
    mode = 'positive' if positive else 'negative'
    if isinstance(positive, bool):
        url += query_template.format(mode=mode)
    if isinstance(pb, tqdm):
        pb.set_description(f'{re.sub("https://hosting101.ru/", "", url)}')
    # Parsing current page
    bs = __parse_page(url)
    if not bs:
        return []
    comment_blocks = bs.find_all('div', class_=f'comment-{mode}')
    content_blocks = [ x.find('div', class_='content') for x in comment_blocks ]
    comments = [ x.find('p').text for x in content_blocks ]
    if delay: 
        sleep(delay[0] + random.random() * (delay[1] - delay[0]))
    if max_pages != None and max_pages <= 1:
        return comments
    # Finding the next page
    pager = bs.find('div', class_='pager')
    if not pager:
        return comments
    next_page_link = pager.find('a', class_='pager-next', recursive=False)
    del comment_blocks, content_blocks, bs
    if next_page_link:
        comments += parse_host(
            url = DOMAIN + next_page_link.get('href'), 
            positive = None,
            delay = delay, 
            max_pages = max_pages - 1 if max_pages != None else None,
            pb = pb
        )

    return comments
