from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_duplicate_registration(driver):
    driver.get("http://127.0.0.1:8000/register")

    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("seleniumuser")
    password.send_keys("Test@123")

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "error"))
    )

    assert error_message.is_displayed()
    assert "Username already exists" in error_message.text

    print("Duplicate registration correctly rejected!")