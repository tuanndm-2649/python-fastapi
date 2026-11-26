"""Request and response schemas for comments."""

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints

from demo_fastapi.constants.comment import (
    COMMENT_CONTENT_MAX_LENGTH,
    COMMENT_CONTENT_MIN_LENGTH,
)
from demo_fastapi.schemas.users import UserPublicResponse


class CommentCreate(BaseModel):
    content: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            max_length=COMMENT_CONTENT_MAX_LENGTH,
            min_length=COMMENT_CONTENT_MIN_LENGTH,
        ),
    ]


class CommentUpdate(CommentCreate):
    pass


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    content: str
    task_id: UUID
    author: UserPublicResponse
