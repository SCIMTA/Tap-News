from selenium.webdriver.common.by import By
import json
import sys
import requests
from common.queue_client import QueueClient

sys.path.append('../')
from utils import convert_timestamp, news_to_json,get_driver
driver = get_driver()


def vnexpress_crawler(nums_of_page):
    url = "https://vnexpress.net/kinh-doanh/bat-dong-san"
    driver.get(url)
    # wait = WebDriverWait(driver, 3)
    articles = []
    for i in range(nums_of_page):
        articles = driver.find_elements(By.CLASS_NAME, 'item-news')
        # articles_more = driver.find_element(By.CLASS_NAME, 'item-news full-thumb article-topstory')
        # articles.append(articles_more)
        print(len(articles))
        for article in articles:
            title = article.find_element(By.CLASS_NAME, 'title-news')
            print(title.text)
            thumb = article.find_element(By.XPATH, './/div//a//picture//source')
            print(thumb.get_property('srcset'))
        driver.execute_script("document.getElementsByClassName('btn-page next-page ')[0].click()")
    driver.close()


def vnexpress_request(limit, page):
    url = "https://gw.vnexpress.net/ar/get_rule_2?category_id=1003181&limit={}&page={}&data_select=title,lead,privacy,thumbnail_url,share_url,article_type,article_category,publish_time&thumb_size=120x72&thumb_quality=100&thumb_dpr=1,2&thumb_fit=crop".format(
        limit, page)

    payload = {}
    headers = {
        'Host': 'gw.vnexpress.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://vnexpress.net',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    return response

def vnexpress_crawler_api(articles_queue:QueueClient):
    limit=40
    page=3
    # parse json
    articles = []
    print("Fetching VNExpress: {} news.".format(limit*page))
    for i in range(page):
        response = vnexpress_request(limit, page)
        data = json.loads(response.text)
        raw_articles = data['data']['1003181']['data']

        for article in raw_articles:
            # new_article_format = {'author': "VNExpress", 'title': article['title'],
            #                       'description': article['lead'],
            #                       'url': article['share_url'], 'urlToImage': article['thumbnail_url'],
            #                       'publishedAt': convert_timestamp(article['publish_time']), 'content': article['lead'],
            #                       'source': {}}
            # new_article_format['source']['id'] = "vnexpress.net"
            # new_article_format['source']['name'] = "VNExpress.net"
            new_article_format = news_to_json("VNExpress", article['title'], article['lead'],
                                               article['share_url'], article['thumbnail_url'],
                                               convert_timestamp(article['publish_time']), article['lead'],
                                               "vnexpress.net", "VNExpress.net")
            articles_queue.sendMessage(new_article_format)
            # articles.append(new_article_format)

    # print(articles)
    return articles

# if __name__ == '__main__':
#     vnexpress_crawler_api(20, 2)
