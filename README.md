
# Selenium Python Automation Framework

## Project Overview

A web application testing and automation framework developed using Python, Selenium WebDriver, and Pytest.

The project includes a user registration and login application built with FastAPI and SQLite. Automated test cases validate application functionality, input validation, authentication scenarios, and browser compatibility.

## Technologies Used

- Python
- Selenium WebDriver
- Pytest
- FastAPI
- SQLite
- HTML
- CSS
- JavaScript
- OpenPyXL
- Pytest HTML Reports

## Key Features

- User registration and login automation
- Page Object Model (POM)
- XPath locator management
- Positive and negative test scenarios
- Data-driven testing using Pytest
- Excel-based test data
- Cross-browser testing using Chrome and Edge
- Password validation and boundary testing
- Automatic failure screenshot capture
- Execution logging
- HTML test reports

## Project Structure

```text
SeleniumPythonFramework/
│
├── login_app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── templates/
│   └── static/
│
├── pages/
│   ├── base_page.py
│   └── login_page.py
│
├── utils/
│   ├── excel_reader.py
│   ├── logger.py
│   └── screenshot.py
│
├── test_data/
│   └── login_data.xlsx
│
├── tests/
│   └── Test files are maintained in the project root
│
├── conftest.py
├── requirements.txt
├── xpath_manager.py
└── README.md
