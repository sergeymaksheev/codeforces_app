from codeforces_app.celery import app
from integration.codeforces.parser import start_problems_task



@app.task
def start_loading_codeforces():
    start_problems_task()
    return "OK"