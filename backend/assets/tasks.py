from celery import shared_task


@shared_task
def debug():
    print("This task works!!")
    pass  # do some long running task
