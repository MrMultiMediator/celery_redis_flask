from celery import shared_task 
from time import sleep

@shared_task(ignore_result=False) #-Line 4
def long_running_task(iterations) -> int:#-Line 5
    result = 0
    for i in range(iterations):
        result += i
        sleep(2) 
    return result #-Line 6
