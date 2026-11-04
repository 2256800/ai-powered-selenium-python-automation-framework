from xpath_manager import XPathManager


def test_multiple_xpath(driver):

    # Open login page
    driver.get(
        "https://practicetestautomation.com/practice-test-login/"
    )

    # Multiple XPath expressions
    xpath_list = [
        "//input[@id='wrong_username']",
        "//input[@name='username']",
        "//input[@id='username']"
    ]

    # Create XPathManager object
    manager = XPathManager(driver)

    # Find username element
    username = manager.find_element(xpath_list)

    # Verify element
    assert username.is_displayed()

    print("Multiple XPath test completed successfully!")