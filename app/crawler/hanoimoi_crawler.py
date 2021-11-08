from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import platform
import sys

sys.path.append('../')
from utils import convert_timestamp, scroll_page, news_to_json, convert_dash_time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

if platform.system() == 'Windows':
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver.exe")
elif platform.system() == 'Linux':
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")


def hanoimoi_crawler(num_of_page):
    url = "http://www.hanoimoi.com.vn/Danh-muc-tin/181/Bat-dong-san"
    driver.get(url)
    wait = WebDriverWait(driver, 3)
    articles = []

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
            articles.append(new_article_format)
        except:
            pass
    # print(articles)
    driver.close()
    return articles