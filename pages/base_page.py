from selenium.common.exceptions import (
    TimeoutException,
    InvalidSelectorException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from xpath_manager import XPathManager


class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

        self.xpath_manager = XPathManager(
            driver,
            timeout=timeout
        )

    def _convert_to_xpath(self, locator):

        by, value = locator

        if by == By.ID:
            return f"//*[@id='{value}']"

        elif by == By.NAME:
            return f"//*[@name='{value}']"

        elif by == By.CLASS_NAME:
            return (
                f"//*[contains(concat(' ', normalize-space(@class), "
                f"' '), ' {value} ')]"
            )

        elif by == By.TAG_NAME:
            return f"//{value}"

        elif by == By.XPATH:
            return value

        return None

    def find_element(self, locator, element_description=None):

        try:
            return self.wait.until(
                EC.presence_of_element_located(locator)
            )

        except (TimeoutException, InvalidSelectorException):

            xpath = self._convert_to_xpath(locator)

            if xpath:
                print("\nActivating AI Smart Locator Recovery...")

                return self.xpath_manager.find_element(
                    xpath_list=xpath,
                    element_description=element_description
                )

            raise

    def wait_for_element(self, locator):
        return self.find_element(locator)

    def click(self, locator, element_description=None):

        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

        except (TimeoutException, InvalidSelectorException):

            element = self.find_element(
                locator,
                element_description
            )

            self.wait.until(
                lambda driver: (
                    element.is_displayed()
                    and element.is_enabled()
                )
            )

        element.click()

    def send_keys(self, locator, text, element_description=None):

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

        except (TimeoutException, InvalidSelectorException):

            element = self.find_element(
                locator,
                element_description
            )

            self.wait.until(
                lambda driver: (
                    element.is_displayed()
                    and element.is_enabled()
                )
            )

        element.send_keys(text)

    def clear(self, locator):
        element = self.find_element(locator)
        element.clear()

    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    def is_displayed(self, locator):
        element = self.find_element(locator)
        return element.is_displayed()