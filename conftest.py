import time
import pytest
from selenium import webdriver

from utils.logger import logger
from ai.ai_failure_analyzer import analyze_test_failure
from ai.ai_execution_report import generate_execution_report


def pytest_addoption(parser):
    parser.addoption(
        "--ai-report",
        action="store_true",
        default=False,
        help="Generate AI execution report using Llama 3"
    )


def pytest_sessionstart(session):
    session.config._ai_report_start_time = time.time()


@pytest.fixture(params=["chrome", "edge"])
def driver(request):

    browser_name = request.param
    logger.info(f"Starting browser: {browser_name}")

    if browser_name == "chrome":
        browser = webdriver.Chrome()

    elif browser_name == "edge":
        browser = webdriver.Edge()

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    try:
        browser.maximize_window()
        yield browser

    finally:
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

            print("\nStarting AI Failure Analysis...")

            analysis = analyze_test_failure(
                test_name=item.name,
                error_message=str(report.longrepr)
            )

            if analysis:
                print("\nAI Failure Analysis:")
                print(analysis)

        elif report.skipped:
            logger.warning(f"SKIPPED: {item.name}")


def pytest_terminal_summary(
    terminalreporter,
    exitstatus,
    config
):

    if not config.getoption("--ai-report"):
        return

    stats = terminalreporter.stats

    passed = len(stats.get("passed", []))
    failed = len(stats.get("failed", []))
    skipped = len(stats.get("skipped", []))

    total = passed + failed + skipped

    start_time = getattr(
        config,
        "_ai_report_start_time",
        time.time()
    )

    duration = time.time() - start_time

    generate_execution_report(
        passed=passed,
        failed=failed,
        skipped=skipped,
        total=total,
        duration=duration
    )