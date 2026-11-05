from xpath_manager import XPathManager


def test_ai_smart_locator_recovery(driver):

    driver.get(
        "https://practicetestautomation.com/practice-test-login/"
    )

    manager = XPathManager(driver, timeout=5)

    # Deliberately incorrect XPath
    wrong_xpath = [
        "//input[@id='incorrect_username']"
    ]

    # Ask AI to recover the username field
    username = manager.find_element(
        xpath_list=wrong_xpath,
        element_description="Username input field on the login page"
    )

    assert username.is_displayed()
    assert username.get_attribute("id") == "username"

    print("\nAI Smart Locator Recovery test passed!")