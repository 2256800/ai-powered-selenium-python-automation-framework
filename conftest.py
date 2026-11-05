import pytest
import os
import re
from datetime import datetime
from selenium import webdriver
from utils.logger import logger
from ai.ai_failure_analyzer import analyze_test_failure


@pytest.fixture(params=["chrome", "edge"])
def driver(request):

    browser_name = request.param
    logger.info(f"Starting browser: {browser_name}")

    if browser_name == "chrome":
        browser = webdriver.Chrome()

    elif browser_name == "edge":
        browser = webdriver.Edge()

    browser.maximize_window()

    yield browser

    browser.quit()
    logger.info(f"Closed browser: {browser_name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    setattr(item, "rep_" + report.when, report)

    if report.when == "call":

        if report.passed:
            logger.info(f"PASSED: {item.name}")

        elif report.failed:
            logger.error(f"FAILED: {item.name}")
            logger.error(str(report.longrepr))

            browser = item.funcargs.get("driver")
            screenshot_path = None

            if browser:
                try:
                    os.makedirs("screenshots", exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    safe_test_name = re.sub(
                        r'[<>:"/\\|?*]',
                        "_",
                        item.name
                    )

                    screenshot_path = (
                        f"screenshots/{safe_test_name}_{timestamp}.png"
                    )

                    browser.save_screenshot(screenshot_path)

                    logger.info(
                        f"Failure screenshot saved: {screenshot_path}"
                    )

                    print(
                        f"\nFailure screenshot saved: {screenshot_path}"
                    )

                except Exception as error:
                    logger.error(f"Screenshot capture failed: {error}")

            # AI-powered failure analysis
            logger.info("Starting AI failure analysis using Llama 3...")

            print("\nStarting AI Failure Analysis...")

            analysis = analyze_test_failure(
                test_name=item.name,
                error_message=str(report.longrepr),
                screenshot_path=screenshot_path
            )

            if analysis:
                logger.info("AI failure analysis completed successfully.")
                print("\nAI Failure Analysis:")
                print(analysis)

        elif report.skipped:
            logger.warning(f"SKIPPED: {item.name}")