from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def fetch_html(channel: str, custom_driver) -> bytes:
    driver = custom_driver.get_driver()
    """Obtiene el archivo html final luego de ser procesado
     por Selenium Webdriver"""
    url = f"https://www.youtube.com/{channel}/videos"
    driver.get(url)
    # Wait until the page has an element with id "video-title"
    # time.sleep(10) # A easier way but static
    _ = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "video-title-link"))
    )

    return driver.page_source.encode("utf-8").strip()


class NoVideosFound(Exception):
    pass
