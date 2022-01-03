from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sys
from common.queue_client import QueueClient

sys.path.append('../')
from utils import convert_not_timestamp, news_to_json, get_driver

driver = get_driver()

def laodong_crawler(articles_queue:QueueClient):
    num_of_page=2

    for i in range(num_of_page):
        url = "https://laodong.vn/tien-te-dau-tu?page={}".format(i+1)
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
                articles_queue.sendMessage(new_article_format)
            except:
                pass

    driver.execute_script("window.close()")