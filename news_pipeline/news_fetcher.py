# -*- coding: utf-8 -*-

import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

from cloudAMQP_client import CloudAMQPClient
import cnn_news_scraper

# DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://xzbggvzn:jFOMw3MZ6hzq0htegQTkG2S7fQsrNby1@chimpanzee.rmq.cloudamqp.com/xzbggvzn"
# DEDUPE_NEWS_TASK_QUEUE_URL = "amqps://fhafmgfc:jx85f69NB8LYHJmUde0IWiTe1KoVdvUy@gerbil.rmq.cloudamqp.com/fhafmgfc"      #redis thanh
DEDUPE_NEWS_TASK_QUEUE_URL = "amqps://gmpzlsjw:MPgc1tkaGgUcqyIfTdTmofNXUuNJMQzy@cattle.rmq2.cloudamqp.com/gmpzlsjw"      #amqp hoang
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"
# SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://hzileycx:iJgtzvRMYnzkdFGSdUYSytpAsW6FYnT_@chimpanzee.rmq.cloudamqp.com/hzileycx"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqps://pizpgglq:Gybn7663NaIbjKwqpWwpXbmZRt5fc0hg@cattle.rmq2.cloudamqp.com/pizpgglq"      #amqp hoang
# SCRAPE_NEWS_TASK_QUEUE_URL = "amqps://crdxxgsm:DKKFtoJFD5nBbyFFqYKCqtoDWearFCuo@gerbil.rmq.cloudamqp.com/crdxxgsm"      #redis thanh
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 1

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if not isinstance(msg, dict):
        print ('message is broken')
        return

    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text

    dedupe_news_queue_client.sendMessage(task)

while True:
    # Fetch msg from queue_name
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                handle_message(msg)
            except Exception as e:
                print ('===============================================================')
                print ('handle_message',e)
                print ('===============================================================')
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
