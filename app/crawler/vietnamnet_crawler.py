import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import platform
import sys

sys.path.append('../')
from utils import convert_not_timestamp, scroll_page, news_to_json, convert_timestamp_hour_min, get_driver

driver = get_driver()

def vietnamnet_crawler(num_of_page):
    articles = []
    for i in range(num_of_page):
        url = "https://vietnamnet.vn/vn/bat-dong-san/trang{}/".format(i+1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)

        # crawling
        raw_articles = driver.find_element(By.CLASS_NAME, 'list-content-loadmore')
        raw_articles = raw_articles.find_elements(By.XPATH, './/div[@class="clearfix item"]')
        print("Fetching Vietnamnet: {} news on page {}.".format(len(raw_articles), i+1))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH, './/a').get_attribute('title')
                description = article.find_element(By.XPATH, './/div//div[@class="lead"]').text
                url = article.find_element(By.XPATH, './/a').get_attribute('href')
                urlToImage = article.find_element(By.XPATH, './/a//img').get_attribute('src')
                publishedAt = article.find_element(By.XPATH, './/div//span[@class="time"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # parse to json
                new_article_format = news_to_json("Vietnamnet", title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "vietnamnet.vn", "Vietnamnet.vn")
                articles.append(new_article_format)
            except:
                pass
        print(len(articles))
        # print(article)
    driver.close()
    return articles