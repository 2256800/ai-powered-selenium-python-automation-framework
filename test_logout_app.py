from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_user_logout(driver):

    # Open login page
    driver.get("http://127.0.0.1:8000/")

    # Enter login credentials
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("seleniumuser")
    password.send_keys("Test@123")

    # Click Login
    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    # Wait for Welcome page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/welcome")
    )

    assert "Welcome" in driver.page_source

    # Click Logout
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Logout']")
        )
    )

    logout_button.click()

    # Verify redirection to Login page
    WebDriverWait(driver, 10).until(
        EC.url_to_be("http://127.0.0.1:8000/")
    )

    assert "Welcome Back!" in driver.page_source

    print("User logout successfully verified!")