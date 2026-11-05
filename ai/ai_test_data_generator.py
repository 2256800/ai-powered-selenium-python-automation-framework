import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"


def generate_test_data(requirement, number_of_records=5):

    if not requirement or not requirement.strip():
        raise ValueError("Requirement cannot be empty.")

    if not isinstance(number_of_records, int) or not 1 <= number_of_records <= 20:
        raise ValueError("Number of records must be between 1 and 20.")

    prompt = f"""
You are an expert Software Test Data Engineer.

Generate {number_of_records} unique synthetic test data records
for the following application requirement:

{requirement}

Return ONLY valid JSON in this structure:

{{
    "test_data": [
        {{
            "test_id": "DATA001",
            "username": "uniqueuser1",
            "password": "Test@123",
            "confirm_password": "Test@123",
            "scenario": "Valid registration",
            "expected_result": "Registration successful"
        }}
    ]
}}

Rules:
1. Generate exactly {number_of_records} records.
2. Use unique usernames.
3. Include positive and negative test scenarios.
4. Include invalid password scenarios where applicable.
5. For valid passwords, follow the specified password rules.
6. For password mismatch scenarios, use different password values.
7. Use only synthetic test data.
8. Do not generate real personal information.
9. Return JSON only. No Markdown.
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

        records = generated_data.get("test_data")

        if not isinstance(records, list) or not records:
            raise ValueError("Invalid AI-generated test data.")

        if len(records) != number_of_records:
            raise ValueError(
                f"Expected {number_of_records} records, "
                f"but received {len(records)}."
            )

        required_fields = {
            "test_id",
            "username",
            "password",
            "confirm_password",
            "scenario",
            "expected_result"
        }

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each test data record must be an object.")

            if not required_fields.issubset(record.keys()):
                raise ValueError("A generated record is missing required fields.")

        print(f"\nAI generated {len(records)} test data records.")

        return records

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
    User registration application.

    Fields:
    - Username: required and unique.
    - Password: minimum 8 characters.
    - Confirm Password: must match the password.

    Invalid registration attempts must display an error message.
    """

    records = generate_test_data(
        requirement,
        number_of_records=5
    )

    if records:
        print("\nAI GENERATED TEST DATA")
        print("=" * 60)

        print(json.dumps(records, indent=4))