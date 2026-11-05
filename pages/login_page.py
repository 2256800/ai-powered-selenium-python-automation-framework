from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):

    URL = "https://practicetestautomation.com/practice-test-login/"

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    ERROR_MESSAGE = (By.ID, "error")
    SUCCESS_MESSAGE = (By.TAG_NAME, "h1")

    def open_login_page(self):
        self.driver.get(self.URL)

    def enter_username(self, username):
        self.send_keys(self.USERNAME, username)

    def enter_password(self, password):
        self.send_keys(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        self.wait.until(
            lambda driver: self.find_element(
                self.ERROR_MESSAGE
            ).text.strip() != ""
        )

        return self.get_text(self.ERROR_MESSAGE).strip()

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)