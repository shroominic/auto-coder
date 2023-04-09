from os import environ
from celery import Celery


celery = Celery("autocoder")

# CONFIG
celery.conf.broker_url = environ.get(
    "CELERY_BROKER_URL", 
    "redis://127.0.0.1:6379/0"
)
celery.conf.result_backend = environ.get(
    "CELERY_RESULT_BACKEND", 
    "rpc://"
)
