from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_successful_login(driver):
    driver.get("http://127.0.0.1:8000/")

    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("seleniumuser")
    password.send_keys("Test@123")

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/welcome")
    )

    assert "Welcome" in driver.page_source
    assert "seleniumuser" in driver.page_source

    print("Successful login verified!")
