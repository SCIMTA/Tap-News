from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sys
from common.queue_client import QueueClient

sys.path.append('../')
from utils import news_to_json, convert_timestamp_hour_min, get_driver

driver = get_driver()

def batdongsan_parser(driver, num_of_page, sub_list, articles_queue):
    for i in range(num_of_page):
        url = "https://batdongsan.com.vn/{}/p{}".format(sub_list, i+1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        container = driver.find_element(By.CLASS_NAME, 're__nlcc-main-content')
        list_articles = container.find_element(By.XPATH, './/div[@class="re__news-listings"]')
        raw_articles = list_articles.find_elements(By.XPATH, './/div[@class="re__news-item"]')
        top_article = raw_articles[0]
        print("Fetching Batdongsan/{}: {} news on page {}.".format(sub_list, len(raw_articles), i+1))
        for article in raw_articles[1:]:
            try:
                title = article.find_element(By.XPATH, './/div[@class="re__news-content"]//h3//a').get_attribute('title')
                description = article.find_element(By.XPATH, './/div[@class="re__news-sapo"]').text
                url = article.find_element(By.XPATH, './/div[@class="re__news-thumb"]//a').get_attribute('href')
                urlToImage = article.find_element(By.XPATH, './/div[@class="re__news-thumb"]//a//img').get_attribute('src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="re__news-time"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # # parse to json
                new_article_format = news_to_json("Batdongsan/{}".format(sub_list), title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
                articles_queue.sendMessage(new_article_format)
            except Exception as err:
                print(err)
                pass

        # Handle top new
        top_new_title = article.find_element(By.XPATH, './/div[@class="re__news-content"]//h3//a').get_attribute('title')
        top_new_description = article.find_element(By.XPATH, './/div[@class="re__news-sapo"]').text
        top_new_url = article.find_element(By.XPATH, './/div[@class="re__news-thumb"]//a').get_attribute('href')
        top_new_urlToImage = article.find_element(By.XPATH, './/div[@class="re__news-thumb"]//a//img').get_attribute('src')
        top_new_publishedAt = article.find_element(By.XPATH, './/div[@class="re__news-time"]').text
        top_new_publishedAt = convert_timestamp_hour_min(top_new_publishedAt)
        top_new = news_to_json("Batdongsan/{}".format(sub_list), top_new_title, top_new_description, top_new_url,
                              top_new_urlToImage, top_new_publishedAt,
                              top_new_description, "batdongsan.com.vn/{}".format(sub_list), "BATDONGSAN.com.vn")
        articles_queue.sendMessage(top_new)
        # print(len(articles))
        # print(article)
    driver.execute_script("window.close()")

def batdongsan_thitruong_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "tin-thi-truong"
    batdongsan_parser(driver, num_of_page, sub_list, articles_queue)


def batdongsan_phantich_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "phan-tich-nhan-dinh"
    batdongsan_parser(driver, num_of_page, sub_list, articles_queue)


def batdongsan_chinhsach_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "chinh-sach-quan-ly"
    batdongsan_parser(driver, num_of_page, sub_list, articles_queue)


def batdongsan_quyhoach_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "thong-tin-quy-hoach"
    batdongsan_parser(driver, num_of_page, sub_list, articles_queue)


def batdongsan_thegioi_crawler(articles_queue:QueueClient):
    num_of_page=2
    driver = get_driver()
    sub_list = "bat-dong-san-the-gioi"
    batdongsan_parser(driver, num_of_page, sub_list, articles_queue)
