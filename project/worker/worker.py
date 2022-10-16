from bs4 import BeautifulSoup
from celery import Celery
from config import settings
from selenium.common.exceptions import TimeoutException
from selenium_session import CustomDriver
from worker.utilities_worker import NoVideosFound, fetch_html

celery = Celery(__name__)


celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend


@celery.task(name="get_videos")
def get_videos(channel: str) -> list[list[str]]:
    try:
        html = fetch_html(channel, CustomDriver())
    except TimeoutException:
        raise NoVideosFound("This channel has no videos or does not exist")

    soup = BeautifulSoup(html, "html.parser")
    common_tag = soup.findAll("a", id="video-title")
    if len(common_tag) > 5:
        common_tag = common_tag[:5]

    titles = [element.get("title") for element in common_tag]
    urls = [element.get("href") for element in common_tag]
    return [titles, urls]


@celery.task(name="close_driver")
def close_driver():
    CustomDriver().close()
    return True
