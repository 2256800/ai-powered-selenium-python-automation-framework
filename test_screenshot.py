from pages.login_page import LoginPage
from utils.screenshot import Screenshot


def test_screenshot_capture(driver):

    login_page = LoginPage(driver)

    login_page.open_login_page()

    screenshot_path = Screenshot.capture(
        driver,
        "login_page"
    )

    assert screenshot_path.endswith(".png")

    print("Screenshot captured successfully!")
