from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
from common.queue_client import QueueClient

sys.path.append('../')
from utils import news_to_json, convert_dash_time, get_driver

driver = get_driver()

def hanoimoi_crawler(articles_queue:QueueClient):
    num_of_page=2
    url = "http://www.hanoimoi.com.vn/Danh-muc-tin/181/Bat-dong-san"
    driver.get(url)
    wait = WebDriverWait(driver, 3)

    # Handle infinitive load
    for i in range(int(num_of_page)*2):
        driver.execute_script("""$('div[class="mediamore main-category-more"] a').click()""")
        time.sleep(0.5)

    # Loading to end to prevent error
    # for i in range(5):
    #     scroll_page(driver)

    # crawling
    raw_article = driver.find_element(By.ID, 'article-cate-more')
    raw_articles = raw_article.find_elements(By.XPATH, '//li[@class]')
    print("Fetching HanoiMoi: {} news.".format(len(raw_articles)))
    for article in raw_articles[:-1]:
        try:
            title = article.find_element(By.XPATH, './/a//h4').text
            # ads filter
            if "TÀI TRỢ" in title:
                continue
            description = article.find_element(By.XPATH, './/p').text
            url = article.find_element(By.XPATH, './/a').get_attribute('href')
            urlToImage = article.find_element(By.XPATH, './/a//span//img').get_attribute('src')
            publishedAt = article.find_element(By.XPATH, './/div[@class="period"]').text
            publishedAt = convert_dash_time(publishedAt)
            # # parse to json
            new_article_format = news_to_json("HanoiMoi", title, description, url,
                                              urlToImage, publishedAt,
                                              description, "hanoimoi.com.vn", "HanoiMoi.com.vn")
            articles_queue.sendMessage(new_article_format)
        except:
            pass
    # print(articles)
    driver.execute_script("window.close()")