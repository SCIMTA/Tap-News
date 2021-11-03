import os
import re
import vnexpress_crawler
import vtvnews_crawler
import laodong_crawler
import vietnamnet_crawler

def get_news_from_crawler():
    articles = []
    # vnexpress = vnexpress_bds.vnexpress_crawler_api(40,3)
    # articles = articles + vnexpress
    # vtvnews = vtvnews_crawler.vtvnews_crawler(5)
    # articles = articles + vtvnews
    # laodong = laodong_crawler.laodong_crawler(5)
    # articles = articles + laodong
    vietnamnet = vietnamnet_crawler.vietnamnet_crawler(3)
    articles = articles + vietnamnet

    print(articles)
    return articles

if __name__ == '__main__':
    a = get_news_from_crawler()
    print(len(a))