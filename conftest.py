import pytest
import os
from datetime import datetime
from selenium import webdriver
from utils.logger import logger


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

            if browser:
                os.makedirs("screenshots", exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                screenshot_name = (
                    f"screenshots/{item.name}_{timestamp}.png"
                )

                browser.save_screenshot(screenshot_name)

                logger.info(f"Failure screenshot saved: {screenshot_name}")
                print(f"\nFailure screenshot saved: {screenshot_name}")

        elif report.skipped:
            logger.warning(f"SKIPPED: {item.name}")
