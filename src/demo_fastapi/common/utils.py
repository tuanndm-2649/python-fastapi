from enum import StrEnum


def enum_check(column: str, enum: type[StrEnum]) -> str:
    values = ", ".join(f"'{item.value}'" for item in enum)

    return f"{column} IN ({values})"
