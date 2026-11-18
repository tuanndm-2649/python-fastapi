"""Request and response schemas for users."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from demo_fastapi.constants.auth import (
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_PATTERN,
)
from demo_fastapi.constants.user import (
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    username: str
    email: EmailStr


class UserRegister(BaseModel):
    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    email: EmailStr
    username: str = Field(
        min_length=USERNAME_MIN_LENGTH, max_length=USERNAME_MAX_LENGTH
    )
    password: str = Field(
        max_length=PASSWORD_MAX_LENGTH,
        min_length=PASSWORD_MIN_LENGTH,
        pattern=PASSWORD_PATTERN,
    )


class UserUpdate(BaseModel):
    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
