from pydantic import BaseModel, Field, field_validator


class UserRegister(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=30
    )

    password: str = Field(
        min_length=8,
        max_length=10
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):
        if not value.strip():
            raise ValueError("Username cannot be empty")

        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 10:
            raise ValueError(
                "Password must contain 8 to 10 characters"
            )

        return value


class UserLogin(BaseModel):

    username: str

    password: str