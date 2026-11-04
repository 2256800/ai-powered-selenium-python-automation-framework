import pytest
from selenium.webdriver.common.by import By


@pytest.mark.parametrize(
    "username, password, expected_valid",
    [
        ("user123", "Test@123", True),
        ("abc", "Password1", True),
        ("ab", "Test@123", False),
        ("user456", "Test1", False),
    ]
)
def test_registration_scenarios(
    driver,
    username,
    password,
    expected_valid
):

    driver.get("http://127.0.0.1:8000/register")

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    username_valid = driver.execute_script(
        "return arguments[0].checkValidity();",
        username_field
    )

    password_valid = driver.execute_script(
        "return arguments[0].checkValidity();",
        password_field
    )

    actual_valid = username_valid and password_valid

    assert actual_valid == expected_valid

    print(
        f"Registration scenario passed: "
        f"{username}, Expected: {expected_valid}"
    )