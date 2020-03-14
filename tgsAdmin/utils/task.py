from tgsServ.celery import app


@app.task
def time_task():
    print("time_task")


@app.task
def time_task2():
    print("time_task2")