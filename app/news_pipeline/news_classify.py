# import classify_bert as cls_bert
import classify_naivebayes as cls_naivebayes
import classify_bert as cls_bert
import sys
from time import time

sys.path.append('./')
from common.queue_client import QueueClient
from task_queue_name import CLASSIFY_NEWS_TASK_QUEUE_NAME, FETCHER_NEWS_TASK_QUEUE_NAME

SLEEP_TIME_IN_SECONDS = 1
# model_nb = cls_naivebayes.load_model()
model_bert = cls_bert.load_model()
classify_queue_client = QueueClient(CLASSIFY_NEWS_TASK_QUEUE_NAME)
fetcher_queue_client = QueueClient(FETCHER_NEWS_TASK_QUEUE_NAME)


##### naive bayes
# def handle_message(news):
#     classify_model, tfidf_model = model_nb
#     text = news['title'] + ' ' + news['content']
#     score = cls_naivebayes.batdongsan_filter(text, classify_model, tfidf_model)
#     print('Classify', news['title'], score)
#     if score > 0.4:
#         fetcher_queue_client.sendMessage(news)
#     else:
#         print("Classify not Bat_dong_san")


#### bert
def handle_message(news):
    model, encoder, tokenizer = model_bert
    text = news['title'] + ' ' + news['content']
    t_start = time()
    predict_label, score = cls_bert.batdongsan_filter_bert(text, model, encoder, tokenizer)
    print("[ANNOUNCE] Predicted success after {} seconds".format(time() - t_start))
    print('[Classify]', news['title'], '| label:', predict_label, '| score: ', score)
    if predict_label == "Bat_dong_san":
        fetcher_queue_client.sendMessage(news)
    else:
        print("[Classify] not Bat_dong_san")

while True:
    msg = classify_queue_client.getMessage()
    if msg is not None:
        # Handle message
        try:
            handle_message(msg)
        except Exception as e:
            print('===============================================================')
            print('Exception classify')
            print(e)
            print('===============================================================')
    classify_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
