from fastapi import FastAPI
from pydantic import BaseModel

class SendMessageModel(BaseModel):
    queue_name: str
    message:dict
app = FastAPI()

list_queue = []
list_queue_name =[]



def check_queue_exist(queue_name):
    try:
        list_queue_name.index(queue_name)
    except ValueError:
        list_queue_name.append(queue_name)
        list_queue.append([])

@app.get("/get_message")
def get_message(queue_name):
    check_queue_exist(queue_name)
    queue = list_queue[list_queue_name.index(queue_name)]
    if queue.__len__() > 0:
            print(f"[O] Received message from {queue_name}")
            message = queue.pop(0)
            return message
    else:
        return None

@app.post("/send_message")
def send_message(body: SendMessageModel):
    message = body.message
    queue_name = body.queue_name
    check_queue_exist(queue_name)
    queue = list_queue[list_queue_name.index(queue_name)]
    queue.append(message)
    return message

@app.get("/get_all_message")
def get_message(queue_name):
    check_queue_exist(queue_name)
    queue = list_queue[list_queue_name.index(queue_name)]
    list_message = []
    while queue.__len__() > 0:
        list_message.append(queue.pop(0))
    return list_message