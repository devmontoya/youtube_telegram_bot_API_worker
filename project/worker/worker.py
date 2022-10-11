import time

from celery import Celery
from config import settings

celery = Celery(__name__)


celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend


@celery.task(name="add_channel")
def add_channel(channel: str):
    print(f"worker {channel}")
    time.sleep(10)
    return True
