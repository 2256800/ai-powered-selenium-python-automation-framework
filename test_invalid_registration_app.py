from selenium.webdriver.common.by import By


def test_short_username_registration(driver):

    driver.get("http://127.0.0.1:8000/register")

    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("ab")
    password.send_keys("Test@123")

    # Check browser validation
    is_valid = driver.execute_script(
        "return arguments[0].checkValidity();",
        username
    )

    assert is_valid is False
    assert username.get_attribute("minlength") == "3"

    print("Short username correctly rejected!")
