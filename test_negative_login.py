from pages.login_page import LoginPage


def test_invalid_username(driver):
    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login("wronguser", "Password123")

    error_message = login_page.get_error_message()

    assert "Your username is invalid!" in error_message

    print("Invalid Username Test Passed!")


def test_invalid_password(driver):
    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login("student", "wrongpassword")

    error_message = login_page.get_error_message()

    assert "Your password is invalid!" in error_message

    print("Invalid Password Test Passed!")