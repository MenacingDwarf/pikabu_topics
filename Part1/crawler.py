"""Crawler script."""
import random
from collections import defaultdict
from random import choice
from time import time
from urllib.parse import quote

import pandas as pd
from bs4 import BeautifulSoup
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from tqdm import tqdm

import sys
sys.path.insert(1, '../src')
from src import PROJECT_PATHS

FIRST_DAY = 2100
LAST_DAY = 4800
DAYS_PORTION = 20
MAX_PAGES = 100
RANDOM_SEED = 137

MIN_LENGTH = 500
DESIRED_POSTS = 10000

with open(f"{PROJECT_PATHS.configs}/crawl_utils/firefox.txt") as file_:
    agents = [x.replace('\n', '') for x in file_.readlines()]


def get_webdriver(ip_proxy, agent):
    """Create webdriver for selenium.

    Webdriver with new proxy and user-agent allows you
    to introduce yourself to the webpage as completely
    new user and hence you won't be blocked.

    Args:
        ip_proxy (str): https proxy ip:port without password.
        agent (str): Firefox user-agent.

    Returns:
        selenium.webdriver: webdriver with embedded proxy and user-agent
    """
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = ip_proxy

    capabilities = webdriver.DesiredCapabilities.FIREFOX
    prox.add_to_capabilities(capabilities)

    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    profile.set_preference("general.useragent.override", agent)

    return webdriver.Firefox(firefox_profile=profile, desired_capabilities=capabilities)


req_proxy = RequestProxy()
proxies = req_proxy.get_proxy_list()

random.seed(RANDOM_SEED)

driver = get_webdriver(choice(proxies).get_address(), choice(agents))
stories = defaultdict(list)

for i, tag in enumerate(PROJECT_PATHS.TAGS):
    tags_url = quote(tag) + quote(',') + quote('текст')
    if tag > 'текст':
        tags_url = quote('текст') + quote(',') + quote(tag)
    current_num = 0
    
    for date in tqdm(reversed(range(FIRST_DAY, LAST_DAY, DAYS_PORTION))):
        if (current_num >= DESIRED_POSTS):
            break
        for page_i in range(1, MAX_PAGES):
            if (current_num >= DESIRED_POSTS):
                break
            try:
                url = f"https://pikabu.ru/tag/{tags_url}?n=2&d={date}&D={date+DAYS_PORTION-1}&page={page_i}"
                driver.get(url)
                bs_page = BeautifulSoup(driver.page_source)
                page = bs_page.find_all(attrs={'class': 'story'})
                if not page:
                    # skip if we reach end of day or get empty page
                    break
                for story in page:
                    try:
                        TEXT = story.find(attrs={'class': 'story__content-inner'}).text.strip()
                        if (len(TEXT) < MIN_LENGTH):
                            continue
                        
                        current_num += 1    
                        TITLE = story.find(attrs={'class': 'story__title'}).text.strip()
                        LIKES = story.find(attrs={'class': 'story__rating-count'}).text.strip()
                        TAGS = "|".join(
                            [x.text for x in story.find_all(attrs={'class': 'tags__tag'})]).strip()
                        try:
                            COMMENTS = story.find(attrs={
                                'class': 'story__comments-link-count'
                            }).text
                        except AttributeError:
                            # thera are no comments for some ads
                            COMMENTS = -1

                        try:
                            VIEWS = story.find(attrs={
                                'class': 'story__views'
                            }).attrs.get('aria-label', 'NO_VIEWS').replace("\xa0",
                                                                           '').split()[0]
                        except AttributeError:
                            # there is no views counter for old stories
                            VIEWS = None

                        NICKNAME = story.find(attrs={'class': 'user__nick'}).text.strip()
                        TIME_GAP = story.find('time').text.strip()
                        TIMESTAMP = story.find('time').attrs['datetime']
                        CURRENT_TIMESTAMP = time()

                        stories['TITLE'].append(TITLE)
                        stories['LIKES'].append(LIKES)
                        stories['TEXT'].append(TEXT)
                        stories['TAGS'].append(TAGS)
                        stories['COMMENTS'].append(COMMENTS)

                        stories['VIEWS'].append(VIEWS)

                        stories['NICKNAME'].append(NICKNAME)
                        stories['TIME_GAP'].append(TIME_GAP)
                        stories['TIMESTAMP'].append(TIMESTAMP)
                        stories['CURRENT_TIMESTAMP'].append(CURRENT_TIMESTAMP)
                    except AttributeError:
                        # skip if we reached ad block of page
                        pass
            except (TimeoutException, WebDriverException):
                # sometimes server losts connection and TimeoutException is raised
                # sometimes proxy comes with required password
                # and WebDriverExceprion is rased
                continue
        
        print(f"Days from {date} to {date+DAYS_PORTION-1} was parsed! Current posts num = {current_num}")
    # safe each day for a separate csv
    df = pd.DataFrame(stories)
    df.to_csv(f"{PROJECT_PATHS.data}\\raw\\date_{PROJECT_PATHS.ENG_TAGS[i]}.csv")
    del (df)
    stories = defaultdict(list)

    driver.close()
    driver = get_webdriver(choice(proxies).get_address(), choice(agents))                