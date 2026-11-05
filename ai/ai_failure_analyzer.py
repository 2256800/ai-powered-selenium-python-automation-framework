import requests
import os
import re
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"


def analyze_test_failure(test_name, error_message):

    short_error = error_message[:2000]

    prompt = f"""
You are an expert Selenium Python Automation Engineer.

Analyze this failed automated test.

Test Name: {test_name}

Error Details:
{short_error}

Provide your analysis in this format:

1. Probable Root Cause
2. Why the Test Failed
3. Recommended Solution
4. Selenium/Python Code Fix (if applicable)

Keep the explanation simple, concise and technical.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 200,
                    "temperature": 0.2
                }
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()
        analysis = result.get(
            "response",
            "No AI analysis generated."
        )

        os.makedirs("ai_reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        safe_test_name = re.sub(
            r'[<>:"/\\|?*]',
            "_",
            test_name
        )

        report_path = (
            f"ai_reports/{safe_test_name}_{timestamp}.txt"
        )

        with open(report_path, "w", encoding="utf-8") as file:
            file.write("AI TEST FAILURE ANALYSIS\n")
            file.write("=" * 50 + "\n\n")
            file.write(f"Test Name: {test_name}\n\n")
            file.write(f"Error Details:\n{short_error}\n\n")
            file.write(f"AI Analysis:\n{analysis}\n")

        print(f"\nAI analysis report saved: {report_path}")

        return analysis

    except requests.exceptions.RequestException as error:
        print(f"\nAI analyzer unavailable: {error}")
        return None

    except Exception as error:
        print(f"\nUnexpected AI analyzer error: {error}")
        return None