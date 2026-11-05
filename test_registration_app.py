
import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_user_registration(driver):
    driver.get("http://127.0.0.1:8000/register")

    wait = WebDriverWait(driver, 10)

    username = wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )

    password = driver.find_element(By.NAME, "password")

    unique_username = "selenium_" + uuid.uuid4().hex[:8]

    username.send_keys(unique_username)
    password.send_keys("Test@123")

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    # Wait for successful redirect or registration error
    wait.until(
        lambda d: (
            d.current_url == "http://127.0.0.1:8000/"
            or len(d.find_elements(By.CLASS_NAME, "error")) > 0
        )
    )

    if driver.current_url == "http://127.0.0.1:8000/":
        print("User registration successful!")
    else:
        errors = driver.find_elements(By.CLASS_NAME, "error")
        print("Registration error:", errors[0].text)
        assert False, "Registration failed: " + errors[0].text

    assert driver.current_url == "http://127.0.0.1:8000/"

