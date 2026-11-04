from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Wait for element
    def wait_for_element(self, locator):

        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        return element

    # Click element
    def click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        element.click()

    # Enter text
    def send_keys(self, locator, text):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        element.send_keys(text)

    # Clear text
    def clear(self, locator):

        element = self.wait_for_element(locator)

        element.clear()

    # Get element text
    def get_text(self, locator):

        element = self.wait_for_element(locator)

        return element.text

    # Check element visibility
    def is_displayed(self, locator):

        element = self.wait_for_element(locator)

        return element.is_displayed()