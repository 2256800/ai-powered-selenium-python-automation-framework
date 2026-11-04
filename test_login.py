from selenium.webdriver.common.by import By


def test_login(driver):

    driver.get("https://practicetestautomation.com/practice-test-login/")

    driver.find_element(By.ID, "username").send_keys("student")

    driver.find_element(By.ID, "password").send_keys("Password123")

    driver.find_element(By.ID, "submit").click()

    assert "logged-in-successfully" in driver.current_url