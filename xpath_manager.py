import json
import re
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
            "Element not found using normal, AI-generated, "
            "or fallback locators."
        )

    def ai_smart_locator(
        self,
        failed_locators,
        element_description=None
    ):

        try:

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
                    aria_label: element.getAttribute('aria-label'),
                    autocomplete: element.getAttribute('autocomplete'),
                    html: element.outerHTML.substring(0, 300)
                }));
            """)

            page_data = json.dumps(
                elements,
                ensure_ascii=False
            )

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

            try:

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
                    timeout=15
                )

                response.raise_for_status()

                ai_response = response.json().get(
                    "response", ""
                )

                generated_data = json.loads(ai_response)

                locators = generated_data.get(
                    "locators", []
                )

                if isinstance(locators, list):

                    for locator in locators[:2]:

                        if not isinstance(locator, dict):
                            continue

                        locator_type = locator.get(
                            "type", ""
                        ).lower()

                        locator_value = locator.get(
                            "value", ""
                        )

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

                        element = self._validate_locator(
                            by,
                            locator_value
                        )

                        if element:
                            print("\nAI SMART LOCATOR SUCCESS!")
                            print(f"Type: {locator_type}")
                            print(f"Value: {locator_value}")

                            return element

            except requests.exceptions.RequestException as error:

                print(
                    f"AI Service Unavailable: {error}"
                )

            except (
                json.JSONDecodeError,
                ValueError,
                TypeError
            ) as error:

                print(
                    f"AI Response Error: {error}"
                )

            # Fallback recovery when AI is unavailable
            print(
                "\nStarting intelligent fallback locator recovery..."
            )

            return self._fallback_locator(
                elements,
                element_description
            )

        except WebDriverException as error:

            print(f"Browser Error: {error}")
            return None

        except Exception as error:

            print(
                f"Unexpected AI Locator Error: {error}"
            )

            return None

    def _validate_locator(self, by, locator_value):

        try:

            found_elements = self.driver.find_elements(
                by,
                locator_value
            )

            if len(found_elements) != 1:
                return None

            return WebDriverWait(
                self.driver,
                self.timeout
            ).until(
                EC.visibility_of(found_elements[0])
            )

        except (
            TimeoutException,
            InvalidSelectorException,
            WebDriverException
        ):

            return None

    def _fallback_locator(
        self,
        elements,
        element_description
    ):

        if not element_description or not elements:
            return None

        description = element_description.lower()

        keywords = set(
            re.findall(r"[a-z0-9]+", description)
        )

        scored_elements = []

        for item in elements:

            score = 0

            attributes = [
                item.get("id", ""),
                item.get("name", ""),
                item.get("placeholder", ""),
                item.get("aria_label", ""),
                item.get("autocomplete", ""),
                item.get("text", "")
            ]

            searchable_text = " ".join(
                str(value).lower()
                for value in attributes
                if value
            )

            for keyword in keywords:

                if keyword in searchable_text:
                    score += 2

            tag = item.get("tag", "").lower()
            input_type = item.get("type", "").lower()

            # Give relevant form elements additional priority.
            if "username" in keywords:

                if (
                    tag == "input"
                    and (
                        "username" in searchable_text
                        or "user" in searchable_text
                    )
                ):
                    score += 5

            if "password" in keywords:

                if (
                    tag == "input"
                    and input_type == "password"
                ):
                    score += 5

            if score > 0:

                scored_elements.append(
                    (score, item)
                )

        if not scored_elements:
            print("Fallback could not identify the element.")
            return None

        scored_elements.sort(
            key=lambda item: item[0],
            reverse=True
        )

        highest_score = scored_elements[0][0]

        best_matches = [
            item
            for score, item in scored_elements
            if score == highest_score
        ]

        # Avoid guessing if multiple elements have the same score.
        if len(best_matches) != 1:

            print(
                "Fallback recovery ambiguous: "
                "multiple elements matched."
            )

            return None

        target = best_matches[0]

        locator_attributes = [
            ("id", target.get("id")),
            ("name", target.get("name"))
        ]

        for attribute, value in locator_attributes:

            if not value:
                continue

            xpath = (
                f"//{target['tag'].lower()}"
                f"[@{attribute}={json.dumps(value)}]"
            )

            element = self._validate_locator(
                By.XPATH,
                xpath
            )

            if element:

                print(
                    "\nFALLBACK LOCATOR RECOVERY SUCCESS!"
                )

                print(f"Recovered XPath: {xpath}")

                return element

        print("Fallback locator validation failed.")

        return None