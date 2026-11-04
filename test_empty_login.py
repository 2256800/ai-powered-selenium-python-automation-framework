from pages.login_page import LoginPage


def test_empty_username_and_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.click_login()

    username = driver.find_element(*login_page.USERNAME)
    password = driver.find_element(*login_page.PASSWORD)

    assert username.get_attribute("value") == ""
    assert password.get_attribute("value") == ""

    print("Empty Username and Password Test Passed!")


def test_empty_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.enter_username("student")
    login_page.click_login()

    password = driver.find_element(*login_page.PASSWORD)
    assert password.get_attribute("value") == ""

    print("Empty Password Test Passed!")


def test_empty_username(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.enter_password("Password123")
    login_page.click_login()

    username = driver.find_element(*login_page.USERNAME)
    assert username.get_attribute("value") == ""

    print("Empty Username Test Passed!")
