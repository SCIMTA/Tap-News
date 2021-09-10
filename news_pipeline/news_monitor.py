# -*- coding: utf-8 -*-

import datetime
import os
import sys
import redis
import hashlib
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import news_api_client
from cloudAMQP_client import CloudAMQPClient

# REDIS_HOST = 'localhost'
REDIS_HOST = '172.29.81.130'        #wsl redis
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24

# SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://hzileycx:iJgtzvRMYnzkdFGSdUYSytpAsW6FYnT_@chimpanzee.rmq.cloudamqp.com/hzileycx"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqps://crdxxgsm:DKKFtoJFD5nBbyFFqYKCqtoDWearFCuo@gerbil.rmq.cloudamqp.com/crdxxgsm"
SCRAPE_NEWS_TASK_QUEUE_NAME = 'tap-news-scrape-news-task-queue'

def concatSources(sourcesList):
    return ','.join(sourcesList)
NEWS_SOURCES = concatSources(['cnn',
                              'bbc-news',
                              'bloomberg',
                              'espn',
                              'nbc-news',
                              'techcrunch',
                              'the-verge',
                              'the-wall-street-journal',
                              'the-new-york-times',
                              'abc-news',
                              'daily-mail',
                              'fox-sports',
                              'the-washington-post'])
print(NEWS_SOURCES)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
SLEEP_TIME_IN_SECONDS = 10

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)

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
