"""Request and response schemas for tags."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from demo_fastapi.constants.tag import TAG_NAME_MAX_LENGTH, TAG_NAME_MIN_LENGTH


class TagBase(BaseModel):
    name: str = Field(min_length=TAG_NAME_MIN_LENGTH, max_length=TAG_NAME_MAX_LENGTH)


class TagResponse(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass
