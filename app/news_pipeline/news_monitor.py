# -*- coding: utf-8 -*-

import datetime
import sys
import redis
import hashlib
import news_classify
import sklearn


# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append('./')

from common import get_news_from_crawler

from common import news_api_client
# import news_api_client
from common.cloudAMQP_client import CloudAMQPClient
# REDIS_HOST = 'localhost'
REDIS_HOST = '192.168.0.2'
# REDIS_HOST = '192.168.145.229'        #wsl redis
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24

# SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://hzileycx:iJgtzvRMYnzkdFGSdUYSytpAsW6FYnT_@chimpanzee.rmq.cloudamqp.com/hzileycx"
# SCRAPE_NEWS_TASK_QUEUE_URL = "amqps://crdxxgsm:DKKFtoJFD5nBbyFFqYKCqtoDWearFCuo@gerbil.rmq.cloudamqp.com/crdxxgsm"      #redis thanh
SCRAPE_NEWS_TASK_QUEUE_URL = "amqps://pizpgglq:Gybn7663NaIbjKwqpWwpXbmZRt5fc0hg@cattle.rmq2.cloudamqp.com/pizpgglq"      #amqp hoang
SCRAPE_NEWS_TASK_QUEUE_NAME = 'tap-news-scrape-news-task-queue'

def concatSources(sourcesList):
    return ','.join(sourcesList)


redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
SLEEP_TIME_IN_SECONDS = 30

classify_model, tfidf_model = news_classify.load_model()


while True:
    news_list_raw = news_api_client.get_news_from_crawler()
    news_list = news_list_raw
    # for news in news_list_raw:
    #     text = news['title'] + ' ' + news['content']
    #     if news_classify.batdongsan_filter(text, classify_model, tfidf_model) > 0.4:
    #         news_list.append(news)

    num_of_new_news = 0

    for news in news_list:
        # temp_title = re.sub(':', '', news['title'])
        
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

        if redis_client.get(news_digest) is None:
            num_of_new_news += 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                # format: YYYY-MM-DDTHH:MM:SSZ in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            # print("news type: ", news)

            redis_client.set(news_digest, str(news))
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print("Fetched {} new news.".format(num_of_new_news))

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
