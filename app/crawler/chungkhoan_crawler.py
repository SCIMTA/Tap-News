from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sys
from common.queue_client import QueueClient

sys.path.append('../')
from utils import news_to_json, convert_timestamp_hour_min, get_driver

driver = get_driver()

def chungkhoan_parser(driver, num_of_page, sub_list, articles_queue):
    for i in range(num_of_page):
        url = "https://vietstock.vn/chung-khoan/{}".format(sub_list, i+1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        # container = driver.find_element(By.CLASS_NAME, 'channel-container')
        # list_articles = container.find_element(By.XPATH, './/div[@class="re__news-listings"]')
        raw_articles = driver.find_elements(By.XPATH, './/div[@id="channel-container"]')
        top_article = raw_articles[0]
        print("Fetching Chung khoan/{}: {} news on page {}.".format(sub_list, len(raw_articles), i+1))
        for article in raw_articles[1:]:
            try:
                title = article.find_element(By.XPATH, './/h2[@class="channel-title"]//a').text
                description = article.find_element(By.XPATH, './/p[@class="visible-md visible-lg"]').text
                url = article.find_element(By.XPATH, './/h2[@class="channel-title"]//a').get_attribute('href')
                urlToImage = article.find_element(By.XPATH, './/div[@class="thumb"]//a//img').get_attribute('src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="meta"]//span[@class="date"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # # parse to json
                new_article_format = news_to_json("Chungkhoan/{}".format(sub_list), title, description, url,
                                                  urlToImage, #publishedAt,
                                                  description, "vietstock.vn/chung-khoan/{}".format(sub_list), "vietstock.vn")
                articles_queue.sendMessage(new_article_format)
            except Exception as err:
                print(err)
                pass

        # # Handle top new
        # top_new_title = article.find_element(By.XPATH, './/div[@class="re__news-content"]//h3//a').get_attribute('title')
        # top_new_description = article.find_element(By.XPATH, './/div[@class="re__news-sapo"]').text
        # top_new_url = article.find_element(By.XPATH, './/div[@class="re__news-thumb"]//a').get_attribute('href')
        # top_new_urlToImage = article.find_element(By.XPATH, './/div[@class="re__news-thumb"]//a//img').get_attribute('src')
        # top_new_publishedAt = article.find_element(By.XPATH, './/div[@class="re__news-time"]').text
        # top_new_publishedAt = convert_timestamp_hour_min(top_new_publishedAt)
        # top_new = news_to_json("Batdongsan/{}".format(sub_list), top_new_title, top_new_description, top_new_url,
        #                       top_new_urlToImage, top_new_publishedAt,
        #                       top_new_description, "vietstock.vn/chung-khoan/{}".format(sub_list), "vietstock.vn")
        # articles_queue.sendMessage(top_new)
        # print(len(articles))
        # print(article)
    driver.execute_script("window.close()")

def chungkhoan_cophieu_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "co-phieu"
    chungkhoan_parser(driver, num_of_page, sub_list, articles_queue)


def chungkhoan_chungkhoanphatsinh_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "chung-khoan-phat-sinh"
    chungkhoan_parser(driver, num_of_page, sub_list, articles_queue)


def chungkhoan_chungquyen_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "chung-quyen"
    chungkhoan_parser(driver, num_of_page, sub_list, articles_queue)


def chungkhoan_traiphieu_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "trai-phieu"
    chungkhoan_parser(driver, num_of_page, sub_list, articles_queue)


def chungkhoan_niemyet_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "niem-yet"
    chungkhoan_parser(driver, num_of_page, sub_list, articles_queue)
