from selenium.webdriver.common.by import By


def test_empty_password_validation(driver):

    driver.get("http://127.0.0.1:8000/register")

    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    # Enter username but leave password empty
    username.send_keys("empty_pass_user")

    # Check browser validation
    is_valid = driver.execute_script(
        "return arguments[0].checkValidity();",
        password
    )

    assert is_valid is False
    assert password.get_attribute("required") is not None

    print("Empty password correctly rejected!")