from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_invalid_password(driver):
    driver.get("http://127.0.0.1:8000/")

    wait = WebDriverWait(driver, 10)

    username = wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )

    password = driver.find_element(By.NAME, "password")

    username.send_keys("seleniumuser")
    password.send_keys("Wrong@123")

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    error_message = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "error"))
    )

    assert error_message.is_displayed()
    assert "Invalid username or password." in error_message.text