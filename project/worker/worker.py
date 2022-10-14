from bs4 import BeautifulSoup
from celery import Celery
from config import settings
from selenium_session import CustomDriver
from worker.utilities_worker import fetch_html

celery = Celery(__name__)


celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend


@celery.task(name="get_videos")
def get_videos(channel: str) -> list[list[str]]:
    html = fetch_html(channel, CustomDriver())
    soup = BeautifulSoup(html, "html.parser")
    common_tag = soup.findAll("a", id="video-title")[:5]
    titles = [element.get("title") for element in common_tag]
    urls = [element.get("href") for element in common_tag]
    return [titles, urls]


@celery.task(name="close_driver")
def close_driver():
    CustomDriver().close()
    return True
