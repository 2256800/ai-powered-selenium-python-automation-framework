import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"


def generate_test_cases(requirement, number_of_cases=5):

    if not requirement or not requirement.strip():
        raise ValueError("Requirement cannot be empty.")

    if not isinstance(number_of_cases, int) or not 1 <= number_of_cases <= 20:
        raise ValueError("Number of test cases must be between 1 and 20.")

    prompt = f"""
You are an expert Selenium Python Automation Engineer.

Generate {number_of_cases} test cases based on the following requirement.

Requirement:
{requirement}

Generate positive, negative, boundary, and validation scenarios
where applicable.

Return ONLY valid JSON using this exact structure:

{{
    "test_cases": [
        {{
            "test_case_id": "TC001",
            "test_scenario": "Scenario description",
            "test_steps": [
                "Step 1",
                "Step 2"
            ],
            "test_data": "Required test data",
            "expected_result": "Expected outcome",
            "priority": "High"
        }}
    ]
}}

Rules:
- Generate exactly {number_of_cases} test cases.
- Use unique test case IDs.
- Keep steps clear and executable.
- Do not include Markdown or explanations outside JSON.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.2,
                    "num_predict": 2000
                }
            },
            timeout=180
        )

        response.raise_for_status()

        result = response.json()
        ai_response = result.get("response", "")

        if not ai_response:
            raise ValueError("Ollama returned an empty response.")

        generated_data = json.loads(ai_response)

        test_cases = generated_data.get("test_cases")

        if not isinstance(test_cases, list):
            raise ValueError("Invalid AI response: test_cases must be a list.")

        if not test_cases:
            raise ValueError("AI did not generate any test cases.")

        print(f"\nAI generated {len(test_cases)} test cases.")

        return test_cases

    except requests.exceptions.RequestException as error:
        print(f"\nOllama connection error: {error}")
        return []

    except (json.JSONDecodeError, ValueError) as error:
        print(f"\nAI response error: {error}")
        return []

    except Exception as error:
        print(f"\nUnexpected error: {error}")
        return []


if __name__ == "__main__":

    requirement = """
    Test a user registration page.

    The page contains username, password and confirm password fields.
    Users should register with valid information.
    Invalid passwords and duplicate usernames should be rejected.
    """

    cases = generate_test_cases(requirement, number_of_cases=5)

    if cases:
        print("\nGENERATED TEST CASES")
        print("=" * 60)

        for case in cases:
            print(json.dumps(case, indent=4))