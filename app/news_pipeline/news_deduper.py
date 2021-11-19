import datetime
import sys
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer
sys.path.append('./')
from common.queue_client import QueueClient
from common import mongodb_client

from task_queue_name import DEDUPE_NEWS_TASK_QUEUE_NAME

SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = 'news'

SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

queue_client = QueueClient(DEDUPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = task['title']
    if text is None:
        return

    # Get all recent news
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(
        published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()

    recent_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin,
                                                                      '$lt': published_at_day_end}}))

    # Handle duplicate news
    if recent_news_list is not None and len(recent_news_list) > 0:
        documents = [str(news['title']) for news in recent_news_list]
        documents.insert(0, text)

        # Calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                # Duplicated news, ignore.
                print('Duplicated news, ignore.')
                return
        db[NEWS_TABLE_NAME].insert_one(task)

    task['publishedAt'] = parser.parse(task['publishedAt'])

    db[NEWS_TABLE_NAME].replace_one(
        {'digest': task['digest']}, task, upsert=True)


while True:
    if queue_client is not None:
        msg = queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print('===============================================================')
                print('Exception dedubper')
                print(e)
                print('===============================================================')
                pass

        queue_client.sleep(SLEEP_TIME_IN_SECONDS)
