"""API routes for tags."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from demo_fastapi.crud.tags import get_tags
from demo_fastapi.database import get_db
from demo_fastapi.schemas.tags import TagResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TagResponse], summary="All tag")
def list_tags(db: Annotated[Session, Depends(get_db)]) -> list[TagResponse]:
    tags = get_tags(db)

    return [TagResponse.model_validate(tag) for tag in tags]
