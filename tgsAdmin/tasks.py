from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time


@shared_task
def time_task():
    # time.sleep(10)
    return "time_task"


def time_task1(str):
    # time.sleep(10)
    print("time_task"+str)



