from selenium.webdriver.common.by import By


def test_valid_boundary_registration(driver):

    driver.get("http://127.0.0.1:8000/register")

    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    # Minimum valid username: 3 characters
    username.send_keys("abc")

    # Minimum valid password: 8 characters
    password.send_keys("Test@123")

    # Verify browser validation
    username_valid = driver.execute_script(
        "return arguments[0].checkValidity();",
        username
    )

    password_valid = driver.execute_script(
        "return arguments[0].checkValidity();",
        password
    )

    assert username_valid is True
    assert password_valid is True

    assert username.get_attribute("minlength") == "3"
    assert password.get_attribute("minlength") == "8"

    print("Valid minimum boundary values accepted!")