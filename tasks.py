from celery import shared_task
from time import sleep

@shared_task(bind=True, ignore_result=False)
def long_running_task(self, iterations) -> int:
    result = 0
    for i in range(iterations):
        result += i
        sleep(2)
        self.update_state(state='RUNNING', meta={'current': i, 'total': iterations})
    return result #-Line 6
