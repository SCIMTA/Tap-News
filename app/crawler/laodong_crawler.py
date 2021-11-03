import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import platform
import sys

sys.path.append('../')
from utils import convert_not_timestamp, scroll_page, news_to_json

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

if platform.system() == 'Windows':
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")
elif platform.system() == 'Linux':
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")


def laodong_crawler(num_of_page):
    articles = []
    for i in range(num_of_page):
        url = "https://laodong.vn/bat-dong-san?page={}".format(i+1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)

        # crawling
        raw_articles = driver.find_element(By.CLASS_NAME, 'list-main-content')
        raw_articles = raw_articles.find_elements(By.XPATH, './/li//article')
        print("Fetching Lao Dong: {} news.".format(len(raw_articles)))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH, './/header//h4//a').text
                description = article.find_elements(By.XPATH, './/p')[-1].text
                url = article.find_element(By.XPATH, './/a').get_attribute('href')
                urlToImage = article.find_element(By.XPATH, './/a//figure//img').get_attribute('data-src')
                publishedAt = article.find_element(By.XPATH, './/p//time').text
                publishedAt = convert_not_timestamp(publishedAt.replace('|', ''))
                # # parse to json
                new_article_format = news_to_json("Lao Dong", title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "laodong.vn", "LaoDong.vn")
                articles.append(new_article_format)
            except:
                pass
        # print(len(articles))

    driver.close()
    return articles