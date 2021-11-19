import hashlib
import redis
import sys
import datetime
sys.path.append('./')
from crawler import main_crawler
from common.queue_client import QueueClient
from task_queue_name import SCRAPE_NEWS_TASK_QUEUE_NAME
REDIS_HOST = 'redis'
# REDIS_HOST = '192.168.0.2'
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24



def concatSources(sourcesList):
    return ','.join(sourcesList)


redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
queue_client = QueueClient(SCRAPE_NEWS_TASK_QUEUE_NAME)
SLEEP_TIME_IN_SECONDS = 1
redis_client.flushall()
while True:
    news_list_raw = main_crawler.get_news_from_crawler()
    news_list = news_list_raw

    num_of_new_news = 0
    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()
        
        if redis_client.get(news_digest) is None:
            num_of_new_news += 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                # format: YYYY-MM-DDTHH:MM:SSZ in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime(
                    '%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, str(news))
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            queue_client.sendMessage(news)
    if num_of_new_news > 0:
        print("Monitor {} new news from crawler".format(num_of_new_news))

    queue_client.sleep(SLEEP_TIME_IN_SECONDS)
