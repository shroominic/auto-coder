from time import sleep
from ..worker import celery


@celery.task(name="healthcheck")
def healthcheck(task_type) -> bool:
    sleep(5)
    return True