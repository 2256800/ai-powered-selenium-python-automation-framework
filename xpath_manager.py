import json
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    InvalidSelectorException,
    NoSuchElementException,
    WebDriverException
)


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"


class XPathManager:

    def __init__(self, driver, timeout=5):
        self.driver = driver
        self.timeout = timeout

    def find_element(self, xpath_list, element_description=None):

        if isinstance(xpath_list, str):
            xpath_list = [xpath_list]

        for xpath in xpath_list:

            try:
                element = WebDriverWait(
                    self.driver,
                    self.timeout
                ).until(
                    EC.presence_of_element_located(
                        (By.XPATH, xpath)
                    )
                )

                print(f"SUCCESS: Element found: {xpath}")
                return element

            except TimeoutException:
                print(f"FAILED: Element not found: {xpath}")

            except InvalidSelectorException:
                print(f"INVALID XPath: {xpath}")

        print("\nStarting AI Smart Locator Recovery...")

        element = self.ai_smart_locator(
            failed_locators=xpath_list,
            element_description=element_description
        )

        if element:
            return element

        raise NoSuchElementException(
            "Element not found using normal or AI-generated locators."
        )

    def ai_smart_locator(
        self,
        failed_locators,
        element_description=None
    ):

        try:
            # Extract only relevant form elements.
            elements = self.driver.execute_script("""
                return Array.from(
                    document.querySelectorAll(
                        'input, button, textarea, select'
                    )
                ).map(element => ({
                    tag: element.tagName,
                    id: element.id,
                    name: element.name,
                    type: element.type,
                    placeholder: element.placeholder,
                    text: element.innerText,
                    html: element.outerHTML.substring(0, 300)
                }));
            """)

            page_data = json.dumps(elements, ensure_ascii=False)

            prompt = f"""
You are a Selenium locator expert.

Find the correct webpage element.

Target: {element_description}

Failed locators: {failed_locators}

Available form elements:
{page_data}

Return JSON only:
{{
  "locators": [
    {{
      "type": "xpath",
      "value": "//input[@id='username']"
    }}
  ]
}}

Rules:
- Return at most 2 locators.
- Identify the exact target.
- Use only attributes shown above.
- Do not invent attributes.
"""

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "keep_alive": "10m",
                    "options": {
                        "temperature": 0,
                        "num_predict": 150,
                        "num_ctx": 2048
                    }
                },
                timeout=120
            )

            response.raise_for_status()

            ai_response = response.json().get("response", "")

            generated_data = json.loads(ai_response)

            locators = generated_data.get("locators", [])

            if not isinstance(locators, list):
                return None

            for locator in locators[:2]:

                if not isinstance(locator, dict):
                    continue

                locator_type = locator.get("type", "").lower()
                locator_value = locator.get("value", "")

                if not isinstance(locator_value, str):
                    continue

                if not locator_value:
                    continue

                if locator_type == "xpath":
                    by = By.XPATH

                elif locator_type == "css":
                    by = By.CSS_SELECTOR

                else:
                    continue

                try:
                    found_elements = self.driver.find_elements(
                        by,
                        locator_value
                    )

                    if len(found_elements) != 1:
                        print(
                            f"Rejected locator: {locator_value}"
                        )
                        continue

                    element = WebDriverWait(
                        self.driver,
                        self.timeout
                    ).until(
                        EC.visibility_of(found_elements[0])
                    )

                    print("\nAI SMART LOCATOR SUCCESS!")
                    print(f"Locator Type: {locator_type}")
                    print(f"Locator Value: {locator_value}")

                    return element

                except (
                    TimeoutException,
                    InvalidSelectorException
                ):
                    print(f"AI locator failed: {locator_value}")

            return None

        except requests.exceptions.RequestException as error:
            print(f"AI Locator Service Error: {error}")
            return None

        except (
            json.JSONDecodeError,
            ValueError,
            TypeError
        ) as error:
            print(f"AI Locator Response Error: {error}")
            return None

        except WebDriverException as error:
            print(f"Browser Error: {error}")
            return None

        except Exception as error:
            print(f"Unexpected AI Locator Error: {error}")
            return None