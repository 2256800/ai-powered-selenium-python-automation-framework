from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)


class DynamicXPath:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    # Using contains()
    def find_by_contains(self, attribute, value):

        xpath = f"//*[contains(@{attribute}, '{value}')]"

        return self._find(xpath)

    # Using starts-with()
    def find_by_starts_with(self, attribute, value):

        xpath = f"//*[starts-with(@{attribute}, '{value}')]"

        return self._find(xpath)

    # Using text()
    def find_by_text(self, text):

        xpath = f"//*[contains(text(), '{text}')]"

        return self._find(xpath)

    # Common method to find elements
    def _find(self, xpath):

        try:
            element = WebDriverWait(
                self.driver,
                self.timeout
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )

            print(f"SUCCESS: Element found using {xpath}")

            return element

        except TimeoutException:
            raise NoSuchElementException(
                f"Element not found: {xpath}"
            )