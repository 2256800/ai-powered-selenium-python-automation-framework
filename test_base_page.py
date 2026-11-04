from selenium.webdriver.common.by import By

from pages.base_page import BasePage


def test_base_page_methods(driver):

    # Open login page
    driver.get(
        "https://practicetestautomation.com/practice-test-login/"
    )

    # Initialize BasePage
    page = BasePage(driver)

    # Username locator
    username = (By.ID, "username")

    # Heading locator
    heading = (By.TAG_NAME, "h2")

    # Test wait_for_element()
    element = page.wait_for_element(username)

    assert element is not None

    # Test is_displayed()
    assert page.is_displayed(username)

    # Test click()
    page.click(username)

    # Test send_keys()
    page.send_keys(username, "student")

    # Test clear()
    page.clear(username)

    # Test get_text()
    heading_text = page.get_text(heading)

    assert heading_text == "Test login"

    print("All BasePage methods executed successfully!")