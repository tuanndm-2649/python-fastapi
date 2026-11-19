from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


USERNAME_PATTERN = r"^[a-z0-9_]+$"

USERNAME_MIN_LENGTH = 1
USERNAME_MAX_LENGTH = 55
NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 100
