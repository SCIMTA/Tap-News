import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import platform
import sys

sys.path.append('../')
from utils import convert_not_timestamp, scroll_page, news_to_json, get_driver

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


def vtvnews_crawler(num_of_page):
    url = "https://vtv.vn/kinh-te/bat-dong-san.htm"
    driver.get(url)
    wait = WebDriverWait(driver, 3)
    articles = []

    # Handle infinitive load
    for i in range(int(num_of_page)*2):
        driver.execute_script("""$('div[class="loadmore"] a[rel="nofollow"]').click()""")
        time.sleep(2)

    # Loading to end to prevent error
    for i in range(5):
        scroll_page(driver)

    # crawling
    top_articles = driver.find_elements(By.XPATH, '//div[@class="focus_left equalheight"]')
    raw_articles = top_articles + driver.find_elements(By.CLASS_NAME, 'tlitem')
    print("Fetching VTVNews: {} news.".format(len(raw_articles)))
    for article in raw_articles[:-1]:
        try:
            title = article.find_element(By.XPATH, './/a').get_attribute('title')
            description = article.find_element(By.XPATH, './/p[@class="sapo"]').text
            url = article.find_element(By.XPATH, './/a').get_attribute('href')
            urlToImage = article.find_element(By.XPATH, './/a//img').get_attribute('src')
            publishedAt = ''
            try:
                publishedAt = article.find_element(By.XPATH, './/div//p[@class="icon_clock"]').text
            except:
                publishedAt = article.find_elements(By.XPATH, './/p[@class="time"]//span')[1].get_attribute('title')
            publishedAt = convert_not_timestamp(publishedAt)
            # parse to json
            new_article_format = news_to_json("VTVNews", title, description, url,
                                              urlToImage, publishedAt,
                                              description, "vtv.vn", "VTV.vn")
            articles.append(new_article_format)
        except:
            pass
    # print(articles)
    driver.close()
    return articles