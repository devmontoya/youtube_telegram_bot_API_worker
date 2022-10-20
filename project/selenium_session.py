import time

from config import settings
from selenium import webdriver


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class CustomDriver(Borg):
    def __init__(self, create_new_instance: bool = True):
        super().__init__()
        if (
            not hasattr(self, "_driver") or self._driver is None
        ) and create_new_instance:
            print("Driver starting")
            options = webdriver.FirefoxOptions()
            options.add_argument("--ignore-ssl-errors=yes")
            options.add_argument("--ignore-certificate-errors")
            # Todo: implement a way to check the status of the session
            time.sleep(5)
            try:
                self._driver = webdriver.Remote(
                    command_executor=f"http://{settings.ip_selenium}:4444/wd/hub",
                    options=options,
                )
            except:
                print("Error while the driver is starting")

    def get_driver(self):
        return self._driver

    def close(self):
        if hasattr(self, "_driver") and self._driver is not None:
            print("Stopping driver")
            self._driver.quit()  # Close driver session and browsers
            self._driver = None
