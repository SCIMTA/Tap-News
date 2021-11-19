
from time import sleep
import requests
import json

queue_host = '0.0.0.0'

class QueueClient:
    queue_name = None
    def __init__(self,  queue_name):
        self.queue_name = queue_name
        
    def sendMessage(self, message):
        url = f"http://{queue_host}:4041/send_message"
        payload = json.dumps({
        "queue_name": self.queue_name,
        "message": message
        })
        headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"[X] Sent message to {self.queue_name}")

    # get a message
    def getMessage(self):
        url = f"http://{queue_host}:4041/get_message?queue_name={self.queue_name}"
        payload={}
        headers = {
        'accept': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_all_message(self):
        url = f"http://{queue_host}:4041/get_all_message?queue_name={self.queue_name}"
        payload={}
        headers = {
        'accept': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()


    # sleep
    def sleep(self, seconds):
        sleep(seconds)
