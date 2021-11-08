import re
import os
import string
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import platform


class BCOLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(
        "user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 11_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4606.211 Safari/537.36'")
    chrome_options.add_argument("--window-size=1280x720")

    if platform.system() == 'Windows':
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")
        # driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
    elif platform.system() == 'Linux':
        # driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./crawler/chromedriver")
    return driver

def convert_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    time_str = pd.to_datetime(str(dt_object))
    return str(time_str)

def convert_timestamp_hour_min(in_time):
    str_time = re.sub("[^0-9]", "", in_time)
    if "phút trước" in in_time:
        return str(pd.Timestamp.now() - pd.Timedelta(hours=1))
    if "giờ trước" in in_time:
        return str(pd.Timestamp.now() - pd.Timedelta(hours=int(str_time)))
    return str(pd.to_datetime(str(in_time)))

def convert_not_timestamp(not_timestamp):
    time_str = pd.to_datetime(str(not_timestamp))
    return str(time_str)

def convert_dash_time(in_time):
    in_time = re.sub('-', '', in_time)
    time_str = pd.to_datetime(in_time)
    return str(time_str)

# selenium only
def scroll_page(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def slow_scroll_page(driver, speed=8):
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

def news_to_json(author, title, description, url, urlToImage, publishedAt, content, source_id, source_name):
    new_article_format = {'author': author, 'title': title,
                          'description': description,
                          'url': url, 'urlToImage': urlToImage,
                          'publishedAt': publishedAt, 'content': content,
                          'source': {}}
    new_article_format['source']['id'] = source_id
    new_article_format['source']['name'] = source_name
    # print(new_article_format)
    return new_article_format