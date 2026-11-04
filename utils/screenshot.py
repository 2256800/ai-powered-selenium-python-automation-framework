import os
from datetime import datetime


class Screenshot:

    @staticmethod
    def capture(driver, test_name):

        screenshot_folder = "screenshots"

        os.makedirs(screenshot_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{test_name}_{timestamp}.png"

        filepath = os.path.join(screenshot_folder, filename)

        driver.save_screenshot(filepath)

        print(f"Screenshot saved: {filepath}")

        return filepath