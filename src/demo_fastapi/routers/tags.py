"""API routes for tags."""

from typing import Annotated

from fastapi import APIRouter, Depends
from redis import Redis
from sqlalchemy.orm import Session

from demo_fastapi.database import get_db
from demo_fastapi.dependencies.cache import get_redis
from demo_fastapi.schemas.tags import TagResponse
from demo_fastapi.services.tags import get_cached_tags

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TagResponse], summary="List tag")
def list_tags(
    db: Annotated[Session, Depends(get_db)],
    cache: Annotated[Redis | None, Depends(get_redis)],
) -> list[TagResponse]:
    return get_cached_tags(db, cache)
