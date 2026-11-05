
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
## AI-Powered Test Failure Analysis

This framework integrates a locally hosted Large Language Model (LLM) using Ollama and Llama 3 to analyze Selenium test failures automatically.

### Key Features

* Automatic detection of failed Pytest test cases.
* Automatic failure screenshot capture.
* AI-powered root cause analysis.
* Explanation of why the test failed.
* Recommended solutions and Selenium/Python code fixes.
* Automatic generation of AI failure analysis reports.
* Local LLM execution without paid API keys.

### Technology Stack

* Python
* Selenium WebDriver
* Pytest
* FastAPI
* Ollama
* Llama 3
* Requests
* Page Object Model (POM)

### AI Failure Analysis Workflow

1. Pytest executes Selenium test cases.
2. When a test fails, the framework captures a screenshot.
3. The failure details are sent to the local Ollama API.
4. Llama 3 analyzes the error.
5. AI generates the probable root cause and recommended solution.
6. The analysis is saved automatically in the `ai_reports/` directory.

### Ollama Setup

Install Ollama and download the model:

```bash
ollama pull llama3:latest
```

Start the Ollama service and run the Selenium test suite:

```bash
pytest -v -s
```

AI-generated reports are stored locally in:

```text
ai_reports/
```

### Project Highlights

This project combines traditional Selenium automation with local AI-powered failure analysis to improve debugging efficiency and provide intelligent insights into automated test failures.

