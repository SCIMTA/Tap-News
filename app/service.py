# import operations
from time import sleep
import operations
import subprocess
from fastapi import FastAPI
app = FastAPI()

# command4 = subprocess.Popen(["uvicorn","queue_service:app","--port","4041","--log-level","critical"])
command4 = subprocess.Popen(["uvicorn","queue_service:app","--host", "0.0.0.0","--port","4041", "--log-level","critical"])
sleep(5)
command1 = subprocess.Popen(["python", "news_pipeline/news_monitor.py"])
command2 = subprocess.Popen(["python", "news_pipeline/news_deduper.py"])
command3 = subprocess.Popen(["python", "news_pipeline/news_fetcher.py"])


@app.get("/getNewsSummariesForUser")
async def _getNewsSummariesForUser(user_id, page_num):
    return operations.getNewsSummariesForUser(user_id, page_num)


@app.get("/logNewsClickForUser")
async def _logNewsClickForUser(user_id, news_id):
    return None
