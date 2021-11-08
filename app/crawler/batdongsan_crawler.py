import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import platform
import sys

sys.path.append('../')
from utils import convert_not_timestamp, scroll_page, news_to_json, \
    convert_timestamp_hour_min, slow_scroll_page

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 11_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4606.211 Safari/537.36'")
chrome_options.add_argument("--window-size=1920x1080")

def get_driver():
    if platform.system() == 'Windows':
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")
    elif platform.system() == 'Linux':
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")
    return driver

def batdongsan_thitruong_crawler(num_of_page):
    driver = get_driver()
    articles = []
    sub_list = "tin-thi-truong"
    for i in range(num_of_page):
        url = "https://batdongsan.com.vn/{}/p{}".format(sub_list, i+1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        container = driver.find_element(By.ID, 'ctl23_BodyContainer')
        list_articles = container.find_element(By.XPATH, './/div[@class="body-left"]')
        raw_articles = list_articles.find_elements(By.XPATH, './/div[@class="tintuc-row1 tintuc-list tc-tit"]')
        print("Fetching Batdongsan/{}: {} news on page {}.".format(sub_list, len(raw_articles), i+1))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH, './/div[@class="tc-img list-news-image-title"]//a').get_attribute('title')
                description = article.find_element(By.XPATH, './/p').text
                url = article.find_element(By.XPATH, './/div[@class="tc-img list-news-image-title"]//a').get_attribute('href')
                urlToImage = article.find_element(By.XPATH, './/div[@class="tc-img list-news-image-title"]//a//img').get_attribute('src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="datetime"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # # parse to json
                new_article_format = news_to_json("Batdongsan/{}".format(sub_list), title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
                articles.append(new_article_format)
            except Exception as err:
                print(err)
                pass
        # Handle top new
        top_new_title = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute('title')
        top_new_description = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//p').text
        top_new_url = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute('href')
        top_new_urlToImage = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-img"]//a//img').get_attribute('src')
        top_new_publishedAt = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//div[@class="datetime"]').text
        top_new_publishedAt = convert_timestamp_hour_min(top_new_publishedAt)
        top_new = news_to_json("Batdongsan/{}".format(sub_list), top_new_title, top_new_description, top_new_url,
                              top_new_urlToImage, top_new_publishedAt,
                              top_new_description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
        articles.append(top_new)
        # print(len(articles))
        # print(article)
    driver.close()
    return articles


def batdongsan_phantich_crawler(num_of_page):
    driver = get_driver()
    articles = []
    sub_list = "phan-tich-nhan-dinh"
    for i in range(num_of_page):
        url = "https://batdongsan.com.vn/{}/p{}".format(sub_list, i + 1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        container = driver.find_element(By.ID, 'ctl23_BodyContainer')
        list_articles = container.find_element(By.XPATH, './/div[@class="body-left"]')
        raw_articles = list_articles.find_elements(By.XPATH, './/div[@class="tintuc-row1 tintuc-list tc-tit"]')
        print("Fetching Batdongsan/{}: {} news on page {}.".format(sub_list, len(raw_articles), i + 1))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH,
                                             './/div[@class="tc-img list-news-image-title"]//a').get_attribute('title')
                description = article.find_element(By.XPATH, './/p').text
                url = article.find_element(By.XPATH, './/div[@class="tc-img list-news-image-title"]//a').get_attribute(
                    'href')
                urlToImage = article.find_element(By.XPATH,
                                                  './/div[@class="tc-img list-news-image-title"]//a//img').get_attribute(
                    'src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="datetime"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # # parse to json
                new_article_format = news_to_json("Batdongsan/{}".format(sub_list), title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "batdongsan.com.vn/{}".format(sub_list),
                                                  "BATDONGSAN.com.vn")
                articles.append(new_article_format)
            except Exception as err:
                print(err)
                pass
        # Handle top new
        top_new_title = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute(
            'title')
        top_new_description = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//p').text
        top_new_url = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute('href')
        top_new_urlToImage = list_articles.find_element(By.XPATH,
                                                        './/div[@class="tt-thumb-img"]//a//img').get_attribute('src')
        top_new_publishedAt = list_articles.find_element(By.XPATH,
                                                         './/div[@class="tt-thumb-cnt"]//div[@class="datetime"]').text
        top_new_publishedAt = convert_timestamp_hour_min(top_new_publishedAt)
        top_new = news_to_json("Batdongsan/{}".format(sub_list), top_new_title, top_new_description, top_new_url,
                               top_new_urlToImage, top_new_publishedAt,
                               top_new_description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
        articles.append(top_new)
        # print(len(articles))
        # print(article)
    driver.close()
    return articles


def batdongsan_chinhsach_crawler(num_of_page):
    driver = get_driver()
    articles = []
    sub_list = "chinh-sach-quan-ly"
    for i in range(num_of_page):
        url = "https://batdongsan.com.vn/{}/p{}".format(sub_list, i + 1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        container = driver.find_element(By.ID, 'ctl23_BodyContainer')
        list_articles = container.find_element(By.XPATH, './/div[@class="body-left"]')
        raw_articles = list_articles.find_elements(By.XPATH, './/div[@class="tintuc-row1 tintuc-list tc-tit"]')
        print("Fetching Batdongsan/{}: {} news on page {}.".format(sub_list, len(raw_articles), i + 1))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH,
                                             './/div[@class="tc-img list-news-image-title"]//a').get_attribute('title')
                description = article.find_element(By.XPATH, './/p').text
                url = article.find_element(By.XPATH, './/div[@class="tc-img list-news-image-title"]//a').get_attribute(
                    'href')
                urlToImage = article.find_element(By.XPATH,
                                                  './/div[@class="tc-img list-news-image-title"]//a//img').get_attribute(
                    'src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="datetime"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # # parse to json
                new_article_format = news_to_json("Batdongsan/{}".format(sub_list), title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "batdongsan.com.vn/{}".format(sub_list),
                                                  "BATDONGSAN.com.vn")
                articles.append(new_article_format)
            except Exception as err:
                print(err)
                pass
        # Handle top new
        top_new_title = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute(
            'title')
        top_new_description = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//p').text
        top_new_url = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute('href')
        top_new_urlToImage = list_articles.find_element(By.XPATH,
                                                        './/div[@class="tt-thumb-img"]//a//img').get_attribute('src')
        top_new_publishedAt = list_articles.find_element(By.XPATH,
                                                         './/div[@class="tt-thumb-cnt"]//div[@class="datetime"]').text
        top_new_publishedAt = convert_timestamp_hour_min(top_new_publishedAt)
        top_new = news_to_json("Batdongsan/{}".format(sub_list), top_new_title, top_new_description, top_new_url,
                               top_new_urlToImage, top_new_publishedAt,
                               top_new_description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
        articles.append(top_new)
        # print(len(articles))
        # print(article)
    driver.close()
    return articles


def batdongsan_quyhoach_crawler(num_of_page):
    driver = get_driver()
    articles = []
    sub_list = "thong-tin-quy-hoach"
    for i in range(num_of_page):
        url = "https://batdongsan.com.vn/{}/p{}".format(sub_list, i + 1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        container = driver.find_element(By.ID, 'ctl23_BodyContainer')
        list_articles = container.find_element(By.XPATH, './/div[@class="body-left"]')
        raw_articles = list_articles.find_elements(By.XPATH, './/div[@class="tintuc-row1 tintuc-list tc-tit"]')
        print("Fetching Batdongsan/{}: {} news on page {}.".format(sub_list, len(raw_articles), i + 1))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH,
                                             './/div[@class="tc-img list-news-image-title"]//a').get_attribute('title')
                description = article.find_element(By.XPATH, './/p').text
                url = article.find_element(By.XPATH, './/div[@class="tc-img list-news-image-title"]//a').get_attribute(
                    'href')
                urlToImage = article.find_element(By.XPATH,
                                                  './/div[@class="tc-img list-news-image-title"]//a//img').get_attribute(
                    'src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="datetime"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # # parse to json
                new_article_format = news_to_json("Batdongsan/{}".format(sub_list), title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "batdongsan.com.vn/{}".format(sub_list),
                                                  "BATDONGSAN.com.vn")
                articles.append(new_article_format)
            except Exception as err:
                print(err)
                pass
        # Handle top new
        top_new_title = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute(
            'title')
        top_new_description = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//p').text
        top_new_url = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute('href')
        top_new_urlToImage = list_articles.find_element(By.XPATH,
                                                        './/div[@class="tt-thumb-img"]//a//img').get_attribute('src')
        top_new_publishedAt = list_articles.find_element(By.XPATH,
                                                         './/div[@class="tt-thumb-cnt"]//div[@class="datetime"]').text
        top_new_publishedAt = convert_timestamp_hour_min(top_new_publishedAt)
        top_new = news_to_json("Batdongsan/{}".format(sub_list), top_new_title, top_new_description, top_new_url,
                               top_new_urlToImage, top_new_publishedAt,
                               top_new_description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
        articles.append(top_new)
        # print(len(articles))
        # print(article)
    driver.close()
    return articles


def batdongsan_thegioi_crawler(num_of_page):
    driver = get_driver()
    articles = []
    sub_list = "bat-dong-san-the-gioi"
    for i in range(num_of_page):
        url = "https://batdongsan.com.vn/{}/p{}".format(sub_list, i + 1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        container = driver.find_element(By.ID, 'ctl23_BodyContainer')
        list_articles = container.find_element(By.XPATH, './/div[@class="body-left"]')
        raw_articles = list_articles.find_elements(By.XPATH, './/div[@class="tintuc-row1 tintuc-list tc-tit"]')
        print("Fetching Batdongsan/{}: {} news on page {}.".format(sub_list, len(raw_articles), i + 1))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH,
                                             './/div[@class="tc-img list-news-image-title"]//a').get_attribute('title')
                description = article.find_element(By.XPATH, './/p').text
                url = article.find_element(By.XPATH, './/div[@class="tc-img list-news-image-title"]//a').get_attribute(
                    'href')
                urlToImage = article.find_element(By.XPATH,
                                                  './/div[@class="tc-img list-news-image-title"]//a//img').get_attribute(
                    'src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="datetime"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # # parse to json
                new_article_format = news_to_json("Batdongsan/{}".format(sub_list), title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "batdongsan.com.vn/{}".format(sub_list),
                                                  "BATDONGSAN.com.vn")
                articles.append(new_article_format)
            except Exception as err:
                print(err)
                pass
        # Handle top new
        top_new_title = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute(
            'title')
        top_new_description = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//p').text
        top_new_url = list_articles.find_element(By.XPATH, './/div[@class="tt-thumb-cnt"]//h2//a').get_attribute('href')
        top_new_urlToImage = list_articles.find_element(By.XPATH,
                                                        './/div[@class="tt-thumb-img"]//a//img').get_attribute('src')
        top_new_publishedAt = list_articles.find_element(By.XPATH,
                                                         './/div[@class="tt-thumb-cnt"]//div[@class="datetime"]').text
        top_new_publishedAt = convert_timestamp_hour_min(top_new_publishedAt)
        top_new = news_to_json("Batdongsan/{}".format(sub_list), top_new_title, top_new_description, top_new_url,
                               top_new_urlToImage, top_new_publishedAt,
                               top_new_description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
        articles.append(top_new)
        # print(len(articles))
        # print(article)
    driver.close()
    return articles