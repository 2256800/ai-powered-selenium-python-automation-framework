import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pwdlib import PasswordHash

from login_app.database import (
    create_users_table,
    create_user,
    get_user
)

password_hash = PasswordHash.recommended()

USERNAME = "seleniumuser"
PASSWORD = "Test@123"


def seed_test_user():
    create_users_table()

    if get_user(USERNAME):
        print("Test user already exists.")
        return

    hashed_password = password_hash.hash(PASSWORD)

    if create_user(USERNAME, hashed_password):
        print("Test user created successfully.")
    else:
        print("Unable to create test user.")


if __name__ == "__main__":
    seed_test_user()