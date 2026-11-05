import os
import requests

from datetime import datetime


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"


def generate_execution_report(
    passed,
    failed,
    skipped,
    total,
    duration
):

    os.makedirs("ai_reports", exist_ok=True)

    summary = f"""
SELENIUM AUTOMATION EXECUTION SUMMARY

Total Tests: {total}
Passed: {passed}
Failed: {failed}
Skipped: {skipped}
Execution Duration: {duration:.2f} seconds
"""

    prompt = f"""
You are an expert Selenium Python Automation Engineer.

Analyze the following test execution results.

{summary}

Generate a concise professional execution report containing:

1. Execution Overview
2. Test Results Analysis
3. Failure Analysis
4. Quality Assessment
5. Recommended Next Steps

Rules:
- Use only the supplied test statistics.
- Do not invent test failures or test names.
- Clearly state when no failures occurred.
- Keep the report concise and professional.
"""

    try:

        print("\nGenerating AI Execution Report using Llama 3...")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0.2,
                    "num_predict": 300,
                    "num_ctx": 2048
                }
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        ai_report = result.get(
            "response",
            "AI report could not be generated."
        )

    except requests.exceptions.RequestException as error:

        print(f"AI Report Service Error: {error}")

        ai_report = (
            "AI analysis unavailable.\n"
            "The following execution statistics were recorded:\n"
            + summary
        )

    except Exception as error:

        print(f"Unexpected Report Error: {error}")

        ai_report = (
            "AI analysis unavailable.\n"
            + summary
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = (
        f"ai_reports/execution_report_{timestamp}.txt"
    )

    with open(report_path, "w", encoding="utf-8") as file:

        file.write(summary)
        file.write("\n\nAI EXECUTION ANALYSIS\n")
        file.write("=" * 50 + "\n\n")
        file.write(ai_report)

    print(f"\nExecution report saved: {report_path}")

    return report_path