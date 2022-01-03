from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
from common.queue_client import QueueClient

sys.path.append('../')
from utils import convert_not_timestamp, scroll_page, news_to_json, get_driver

driver = get_driver()



def vneconomy_crawler(articles_queue:QueueClient):
    num_of_page=2
    for i in range(num_of_page):
        url = "https://vneconomy.vn/chung-khoan.htm?trang={}".format(i+1)
    driver.get(url)
    wait = WebDriverWait(driver, 3)

    # Loading to end to prevent error
    for i in range(5):
        scroll_page(driver)

    # crawling
    raw_articles = driver.find_elements(By.CLASS_NAME, 'column-border')
    print("Fetching vneconomy : {} news.".format(len(raw_articles)))
    for article in raw_articles[:-1]:
        try:
            title = article.find_element(By.XPATH, './/h3//a').get_attribute('title')
            description = article.find_element(By.XPATH, './/div//a').text
            url = article.find_element(By.XPATH, './/div//a').get_attribute('href')
            urlToImage = article.find_element(By.XPATH, './/figure//a//img').get_attribute('src')
            publishedAt = ''
            publishedAt = article.find_elements(By.XPATH, './/header//div//time').text
            publishedAt = convert_not_timestamp(publishedAt)
            # parse to json
            new_article_format = news_to_json("VneconomyNews", title, description, url,
                                               urlToImage, publishedAt,
                                              description, "VnEconomy.vn", "vneconomy.vn")
            articles_queue.sendMessage(new_article_format)
        except:
            pass
    driver.execute_script("window.close()")