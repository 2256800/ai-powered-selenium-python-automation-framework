from dynamic_xpath import DynamicXPath


def test_dynamic_xpath(driver):

    # Open login page
    driver.get(
        "https://practicetestautomation.com/practice-test-login/"
    )

    # Initialize Dynamic XPath
    dynamic = DynamicXPath(driver)

    # Locate username using contains()
    username = dynamic.find_by_contains(
        "id", "user"
    )

    assert username.is_displayed()

    # Locate login button using starts-with()
    login_button = dynamic.find_by_starts_with(
        "id", "submit"
    )

    assert login_button.is_displayed()

    print("Dynamic XPath test completed successfully!")