import pytest
from pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("student", "Password123", "Logged In Successfully"),
        ("wronguser", "Password123", "Your username is invalid!"),
        ("student", "wrongpassword", "Your password is invalid!"),
    ]
)
def test_login_scenarios(driver, username, password, expected_message):

    login_page = LoginPage(driver)

    login_page.open_login_page()
    login_page.login(username, password)

    if expected_message == "Logged In Successfully":
        actual_message = login_page.get_success_message()
    else:
        actual_message = login_page.get_error_message()

    assert actual_message == expected_message

    print(f"\nLogin scenario passed: {username}")
