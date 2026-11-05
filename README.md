# AI-Powered Selenium Python Automation Framework

## Project Overview

An intelligent web application testing framework built using Python, Selenium WebDriver, Pytest, and locally hosted Large Language Models (LLMs).

The framework combines traditional browser automation with AI-powered capabilities to assist with test case generation, test data generation, smart locator recovery, failure analysis, and execution reporting.

A sample registration and login application is developed using FastAPI and SQLite to demonstrate automated testing.

AI capabilities are powered by **Ollama and Llama 3**, allowing local LLM integration without requiring external AI API keys.

## Technologies Used

* Python 3.12
* Selenium WebDriver
* Pytest
* FastAPI
* SQLite
* Ollama
* Llama 3
* Requests
* OpenPyXL
* Pytest HTML
* Page Object Model (POM)
* Git and GitHub
* GitHub Actions

## Key Features

### Selenium Automation

* Automated user registration and login.
* Positive and negative test scenarios.
* Page Object Model architecture.
* XPath and CSS locator management.
* Explicit waits and element interaction.
* Cross-browser testing using Chrome and Edge.
* Excel-based data-driven testing.
* Password validation and boundary testing.
* Structured execution logging.

### AI-Powered Capabilities

* AI-powered test case generation.
* AI-powered test data generation.
* AI Smart Locator Recovery using Llama 3.
* AI-driven test failure analysis.
* AI-generated execution summary reports.
* Local LLM integration using Ollama.

### Reporting and CI

* Pytest HTML execution reports.
* Text-based AI analysis reports.
* Structured application logs.
* GitHub Actions CI integration.

## AI-Powered Capabilities

### 1. AI Test Case Generator

Generates test scenarios from a user-provided requirement.

Generated information includes:

* Test Case ID
* Test Scenario
* Test Steps
* Test Data
* Expected Result
* Priority

### 2. AI Test Data Generator

Generates synthetic test data for different testing scenarios, including:

* Valid registration data.
* Invalid password scenarios.
* Password mismatch scenarios.
* Positive and negative test inputs.

Generated data is validated for required fields and record count. As with any LLM-generated output, its semantic correctness should be reviewed before use.

### 3. AI Smart Locator Recovery

When a normal Selenium XPath locator fails:

1. Selenium attempts to locate the element.
2. The framework activates AI Smart Locator Recovery.
3. Relevant webpage form-element information is collected.
4. The information is sent to the local Ollama API.
5. Llama 3 suggests alternative XPath or CSS locators.
6. The framework validates the suggested locator.
7. A unique, visible element is returned if validation succeeds.

This feature helps recover from certain locator changes without immediately modifying the test.

### 4. AI Test Failure Analysis

When an automated test fails:

1. Pytest detects the failure.
2. The framework collects the test name and error details.
3. Error information is sent to the local Ollama API.
4. Llama 3 analyzes the failure.
5. AI identifies the probable root cause.
6. AI recommends solutions and possible Selenium/Python code fixes.
7. The analysis is saved in the `ai_reports` directory.

The analyzer provides:

* Probable Root Cause
* Why the Test Failed
* Recommended Solution
* Selenium/Python Code Fix

### 5. AI Execution Report Generator

Generates an AI-assisted execution summary containing:

* Total tests executed.
* Passed tests.
* Failed tests.
* Skipped tests.
* Execution duration.
* Test result analysis.
* Quality assessment.
* Recommended next steps.

The report is saved as a text file in `ai_reports`.

## Project Architecture

The framework follows a modular architecture:

**Test Scripts → Pytest → Page Object Model → Selenium WebDriver → Web Application**

AI integrations support the automation workflow:

* XPath failure → AI Smart Locator Recovery.
* Test failure → AI Failure Analyzer.
* Test requirement → AI Test Case Generator.
* Test data requirement → AI Test Data Generator.
* Test execution summary → AI Execution Report Generator.

## Project Structure

```text
SeleniumPythonFramework/
|
|-- ai/
|   |-- ai_failure_analyzer.py
|   |-- ai_execution_report.py
|   |-- ai_test_case_generator.py
|   |-- ai_test_data_generator.py
|
|-- login_app/
|   |-- main.py
|   |-- database.py
|   |-- models.py
|   |-- templates/
|   |-- static/
|
|-- pages/
|   |-- base_page.py
|   |-- login_page.py
|
|-- utils/
|   |-- excel_reader.py
|   |-- logger.py
|
|-- scripts/
|   |-- seed_test_user.py
|
|-- test_data/
|   |-- login_data.xlsx
|
|-- ai_reports/
|
|-- tests/
|   |-- Selenium and Pytest test modules
|
|-- conftest.py
|-- xpath_manager.py
|-- requirements.txt
|-- README.md
|
|-- .github/
    |-- workflows/
        |-- selenium-tests.yml
```

*Note: The project structure above highlights the main modules; individual test files may be located in the project root.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/2256800/selenium-python-automation-framework.git
```

```bash
cd selenium-python-automation-framework
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

Install Ollama and download the Llama 3 model:

```bash
ollama pull llama3:latest
```

Ensure the Ollama service is running before using AI-powered features.

### 5. Start the FastAPI Application

Open a terminal in the project directory:

```bash
uvicorn login_app.main:app --reload
```

The application will be available at:

`http://127.0.0.1:8000/`

Keep the application running while executing tests that use the local login application.

## Running Tests

Open a second terminal, activate the virtual environment, and run:

### Run the Complete Test Suite

```bash
python -m pytest -v
```

### Generate an AI Execution Report

```bash
python -m pytest -v --ai-report
```

### Run a Specific Test Module

```bash
python -m pytest -v test_login_pom.py
```

### Generate AI Test Cases

```bash
python -m ai.ai_test_case_generator
```

### Generate AI Test Data

```bash
python -m ai.ai_test_data_generator
```

## Reports and Logs

The framework generates:

| Output               | Location                       |
| -------------------- | ------------------------------ |
| AI Failure Analysis  | `ai_reports/`                  |
| AI Execution Reports | `ai_reports/`                  |
| Execution Logs       | `logs/test_execution.log`      |
| Pytest HTML Reports  | Configured through Pytest HTML |

## Continuous Integration

GitHub Actions is configured to execute the Selenium test suite automatically.

The CI workflow:

* Sets up Python.
* Installs project dependencies.
* Starts the FastAPI application.
* Prepares test data.
* Executes automated tests.

Local Ollama-based AI features require a running Ollama service and are not guaranteed to be available in the GitHub Actions environment.

## Project Objective

The objective of this project is to demonstrate how traditional Selenium automation can be enhanced with locally hosted AI capabilities to improve test development, locator recovery, failure investigation, and execution reporting.

## Author

**Poojitha Manipati**

GitHub: https://github.com/2256800
