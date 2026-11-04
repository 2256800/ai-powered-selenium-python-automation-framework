import uuid


def test_user_registration(driver):
    driver.get("http://127.0.0.1:8000/register")

    username = driver.find_element("name", "username")
    password = driver.find_element("name", "password")

    unique_username = "selenium_" + uuid.uuid4().hex[:8]

    username.send_keys(unique_username)
    password.send_keys("Test@123")

    driver.find_element(
        "css selector",
        "button[type='submit']"
    ).click()

    print("Current URL:", driver.current_url)

    errors = driver.find_elements("class name", "error")

    if errors:
        print("Registration error:", errors[0].text)

    assert driver.current_url == "http://127.0.0.1:8000/"

    print("User registration successful!")
