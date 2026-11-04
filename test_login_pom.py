from pages.login_page import LoginPage


def test_valid_login(driver):
    login_page = LoginPage(driver)

    # Open login page
    login_page.open_login_page()

    # Enter valid credentials and login
    login_page.login("student", "Password123")

    # Verify successful login
    success_message = login_page.get_success_message()

    assert success_message == "Logged In Successfully"

    print("POM Login Test Passed Successfully!")