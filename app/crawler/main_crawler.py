import os
import re
import time

import vnexpress_crawler
import vtvnews_crawler
import laodong_crawler
import vietnamnet_crawler
import thanhnien_crawler
import hanoimoi_crawler
import batdongsan_crawler

def get_news_from_crawler():
    articles = []
    vnexpress = vnexpress_crawler.vnexpress_crawler_api(40,3)
    articles = articles + vnexpress
    vtvnews = vtvnews_crawler.vtvnews_crawler(5)
    articles = articles + vtvnews
    laodong = laodong_crawler.laodong_crawler(5)
    articles = articles + laodong
    vietnamnet = vietnamnet_crawler.vietnamnet_crawler(8)
    articles = articles + vietnamnet
    thanhnien = thanhnien_crawler.thanhnien_crawler(5)
    articles = articles + thanhnien
    hanoimoi = hanoimoi_crawler.hanoimoi_crawler(1)
    articles = articles + hanoimoi
    batdongsan_thitruong = batdongsan_crawler.batdongsan_thitruong_crawler(5)
    articles = articles + batdongsan_thitruong
    batdongsan_phantich = batdongsan_crawler.batdongsan_phantich_crawler(5)
    articles = articles + batdongsan_phantich
    batdongsan_chinhsach = batdongsan_crawler.batdongsan_chinhsach_crawler(5)
    articles = articles + batdongsan_chinhsach
    batdongsan_quyhoach = batdongsan_crawler.batdongsan_quyhoach_crawler(5)
    articles = articles + batdongsan_quyhoach
    batdongsan_thegioi = batdongsan_crawler.batdongsan_thegioi_crawler(5)
    articles = articles + batdongsan_thegioi

    print("Fetch {} news from crawler...........".format(len(articles)))
    return articles


# if __name__ == '__main__':
#     a = get_news_from_crawler()
#     print(len(a))