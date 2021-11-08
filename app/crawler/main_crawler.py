import os
import re
import time
import sys

sys.path.append('./')
from . import vnexpress_crawler
from . import vtvnews_crawler
from . import laodong_crawler
from . import vietnamnet_crawler
from . import thanhnien_crawler
from . import hanoimoi_crawler
from . import batdongsan_crawler

def get_news_from_crawler():
    articles = []
    vnexpress = vnexpress_crawler.vnexpress_crawler_api(40,3)
    articles = articles + vnexpress
    vtvnews = vtvnews_crawler.vtvnews_crawler(2)
    articles = articles + vtvnews
    laodong = laodong_crawler.laodong_crawler(2)
    articles = articles + laodong
    vietnamnet = vietnamnet_crawler.vietnamnet_crawler(2)
    articles = articles + vietnamnet
    thanhnien = thanhnien_crawler.thanhnien_crawler(2)
    articles = articles + thanhnien
    hanoimoi = hanoimoi_crawler.hanoimoi_crawler(2)
    articles = articles + hanoimoi
    batdongsan_thitruong = batdongsan_crawler.batdongsan_thitruong_crawler(2)
    articles = articles + batdongsan_thitruong
    batdongsan_phantich = batdongsan_crawler.batdongsan_phantich_crawler(2)
    articles = articles + batdongsan_phantich
    batdongsan_chinhsach = batdongsan_crawler.batdongsan_chinhsach_crawler(2)
    articles = articles + batdongsan_chinhsach
    batdongsan_quyhoach = batdongsan_crawler.batdongsan_quyhoach_crawler(2)
    articles = articles + batdongsan_quyhoach
    batdongsan_thegioi = batdongsan_crawler.batdongsan_thegioi_crawler(2)
    articles = articles + batdongsan_thegioi

    print("Fetch {} news from crawler...........".format(len(articles)))
    return articles


if __name__ == '__main__':
    a = get_news_from_crawler()
    print(len(a))