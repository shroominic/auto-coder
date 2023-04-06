from os import environ
from celery import Celery


celery = Celery("autocoder")

# CONFIG
celery.conf.broker_url = environ.get(
    "CELERY_BROKER_URL", 
    "rabbitmq://localhost:5672"
)
celery.conf.result_backend = environ.get(
    "CELERY_RESULT_BACKEND", 
    "rabbitmq://localhost:5672"
)
