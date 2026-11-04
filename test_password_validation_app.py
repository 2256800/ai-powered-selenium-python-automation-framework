def test_long_password_registration(driver):
    driver.get("http://127.0.0.1:8000/register")

    username = driver.find_element("name", "username")
    password = driver.find_element("name", "password")

    username.send_keys("longpassuser")
    password.send_keys("TestPassword123")

    entered_password = password.get_attribute("value")

    assert len(entered_password) == 10
    assert password.get_attribute("maxlength") == "10"

    print("Maximum password length correctly restricted to 10 characters!")
def test_short_password_registration(driver):
    driver.get("http://127.0.0.1:8000/register")

    username = driver.find_element("name", "username")
    password = driver.find_element("name", "password")

    username.send_keys("shortpassuser")
    password.send_keys("Test1")

    is_valid = driver.execute_script(
        "return arguments[0].checkValidity();",
        password
    )

    assert is_valid is False
    assert password.get_attribute("minlength") == "8"

    print("Short password correctly rejected!")
