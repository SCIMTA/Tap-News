import json
import pickle
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

from common import mongodb_client
NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 150
USER_NEWS_TIME_OUT_IN_SECONDS = 60

NEWS_TABLE_NAME = 'news'
REDIS_HOST = 'redis'
# REDIS_HOST = '192.168.0.2'
REDIS_PORT = 6379

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # The final list of news to be returned.
    sliced_news = []
    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digest = news_digests[begin_index:end_index]
        sliced_news = list(db[NEWS_TABLE_NAME].find(
            {'digest': {'$in': sliced_news_digest}}))
    else:
        total_news = list(db[NEWS_TABLE_NAME].find().sort(
            [('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digest = [x['digest'] for x in total_news]

        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    return json.loads(dumps(sliced_news))
