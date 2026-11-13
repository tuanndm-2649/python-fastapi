from collections.abc import Sequence
from typing import Self

from pydantic import BaseModel, Field, computed_field

from demo_fastapi.constants.pagination import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    MIN_PAGE,
    MIN_PAGE_SIZE,
)


class PaginationParams(BaseModel):
    page: int = Field(default=DEFAULT_PAGE, ge=MIN_PAGE)
    page_size: int = Field(
        default=DEFAULT_PAGE_SIZE, ge=MIN_PAGE_SIZE, le=MAX_PAGE_SIZE
    )

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PageResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    page_size: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size

    @classmethod
    def from_result(
        cls, items: Sequence[object], total: int, pagination: PaginationParams
    ) -> Self:
        return cls.model_validate(
            {
                "items": items,
                "total": total,
                "page": pagination.page,
                "page_size": pagination.page_size,
            }
        )
