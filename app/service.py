# import operations
import operations
import subprocess

from fastapi import FastAPI
app = FastAPI()


# command1 = subprocess.Popen([ "python","news_pipeline/news_monitor.py" ])
# command2 = subprocess.Popen([ "python","news_pipeline/news_deduper.py" ])
# command3 = subprocess.Popen([ "python","news_pipeline/news_fetcher.py" ])

@app.get("/getNewsSummariesForUser")
async def _getNewsSummariesForUser(user_id, page_num):
    return operations.getNewsSummariesForUser(user_id, page_num)


@app.get("/logNewsClickForUser")
async def _logNewsClickForUser(user_id, news_id):
    return operations.logNewsClickForUser(user_id, news_id)