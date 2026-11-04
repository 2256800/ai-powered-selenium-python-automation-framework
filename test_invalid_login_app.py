def test_invalid_password(driver):
    driver.get("http://127.0.0.1:8000/")

    username = driver.find_element("name", "username")
    password = driver.find_element("name", "password")

    username.send_keys("seleniumuser")
    password.send_keys("Wrong@123")

    driver.find_element("css selector", "button[type='submit']").click()

    error_message = driver.find_element("class name", "error")

    assert error_message.is_displayed()
    assert "Invalid username or password" in error_message.text
