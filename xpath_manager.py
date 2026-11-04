from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    InvalidSelectorException,
    NoSuchElementException
)


class XPathManager:

    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.timeout = timeout

    def find_element(self, xpath_list):

        for xpath in xpath_list:

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
                print(f"FAILED: Element not found using {xpath}")

            except InvalidSelectorException:
                print(f"INVALID XPath: {xpath}")

        raise NoSuchElementException(
            "Element not found using any provided XPath."
        )