import operations
SERVER_HOST = 'localhost'
SERVER_PORT = 4040
from fastapi import FastAPI
app = FastAPI()


@app.get("/getNewsSummariesForUser")
async def _getNewsSummariesForUser(user_id, page_num):
    return operations.getNewsSummariesForUser(user_id, page_num)


@app.get("/logNewsClickForUser")
async def _logNewsClickForUser(user_id, news_id):
    return operations.logNewsClickForUser(user_id, news_id)