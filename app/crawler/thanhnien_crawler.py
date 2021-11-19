from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sys
from common.queue_client import QueueClient

sys.path.append('../')
from utils import news_to_json, convert_timestamp_hour_min, get_driver

driver = get_driver()

def thanhnien_crawler(articles_queue:QueueClient):
    num_of_page=2
    for i in range(num_of_page):
        url = "https://thanhnien.vn/tai-chinh-kinh-doanh/dia-oc/?trang={}".format(i+1)
        print(url)
        driver.get(url)
        wait = WebDriverWait(driver, 3)
        # slow_scroll_page(driver, 13)

        # crawling
        raw_articles = driver.find_element(By.CLASS_NAME, 'relative')
        raw_articles = raw_articles.find_elements(By.XPATH, './/article[@class="story"]')
        print("Fetching Thanhnien: {} news on page {}.".format(len(raw_articles), i+1))
        for article in raw_articles:
            try:
                title = article.find_element(By.XPATH, './/a').get_attribute('title')
                description = article.find_element(By.XPATH, './/div[@class="summary"]//p').text
                url = article.find_element(By.XPATH, './/a').get_attribute('href')
                urlToImage = article.find_element(By.XPATH, './/a//img').get_attribute('data-src')
                publishedAt = article.find_element(By.XPATH, './/div[@class="meta"]//span[@class="time"]').text
                publishedAt = convert_timestamp_hour_min(publishedAt)
                # # parse to json
                new_article_format = news_to_json("Thanhnien", title, description, url,
                                                  urlToImage, publishedAt,
                                                  description, "thanhnien.vn", "THANHNIEN.vn")
                articles_queue.sendMessage(new_article_format)
            except:
                pass
        # print(article)
    driver.close()