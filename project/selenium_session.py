import time

from selenium import webdriver


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class CustomDriver(Borg):

    def __init__(self, name=None):
        super().__init__()
        if not hasattr(self, "_driver") or self._driver is None:
            print("Driver starting")
            options = webdriver.FirefoxOptions()
            options.add_argument("--ignore-ssl-errors=yes")
            options.add_argument("--ignore-certificate-errors")
            time.sleep(10)  # Todo: implement a way to check the status of the session
            try:
                self._driver = webdriver.Remote(
                    command_executor="http://172.18.0.3:4444/wd/hub", options=options
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
