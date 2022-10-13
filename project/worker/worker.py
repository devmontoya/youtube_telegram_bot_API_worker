import time

from bs4 import BeautifulSoup
from celery import Celery
from config import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_session import CustomDriver

celery = Celery(__name__)


celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend


@celery.task(name="get_videos")
def get_videos(channel: str) -> list[list[str]]:
    driver = CustomDriver().get_driver()
    """Obtiene el archivo html final luego de ser procesado
     por Selenium Webdriver"""
    url = f"https://www.youtube.com/{channel}/videos"
    driver.get(url)
    # Wait until the page has an element with id "video-title"
    # time.sleep(10) # A easier way but static
    _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video-title"))
    )

    html = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(html, "html.parser")
    common_tag = soup.findAll("a", id="video-title")[:5]
    titles = [element.get("title") for element in common_tag]
    urls = [element.get("href") for element in common_tag]
    return [titles, urls]


@celery.task(name="close_driver")
def close_driver():
    CustomDriver().close()
    return True
