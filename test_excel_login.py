import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.excel_reader import read_login_data


login_data = read_login_data("test_data/login_data.xlsx")


@pytest.mark.parametrize(
    "username, password, expected_result",
    login_data
)
def test_excel_login(driver, username, password, expected_result):

    driver.get("http://127.0.0.1:8000/")

    driver.find_element(
        By.NAME, "username"
    ).send_keys(username)

    driver.find_element(
        By.NAME, "password"
    ).send_keys(password)

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            expected_result
        )
    )

    assert expected_result in driver.page_source

    print(f"Excel login scenario passed: {username}")
