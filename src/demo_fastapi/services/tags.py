import logging

from pydantic import TypeAdapter, ValidationError
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy.orm import Session

from demo_fastapi.constants.message import (
    FAILED_TO_READ_TAGS_CACHE,
    FAILED_TO_WRITE_TAGS_CACHE,
)
from demo_fastapi.constants.tag import TAGS_CACHE_KEY, TAGS_CACHE_TTL
from demo_fastapi.crud.tags import get_tags
from demo_fastapi.schemas.tags import TagResponse

logger = logging.getLogger(__name__)
tags_adapter = TypeAdapter(list[TagResponse])


def get_cached_tags(db: Session, cache: Redis | None) -> list[TagResponse]:
    if cache is not None:
        try:
            cached_tags = cache.get(TAGS_CACHE_KEY)
            if cached_tags is not None:
                return tags_adapter.validate_json(cached_tags)
        except RedisError, ValidationError:
            logger.warning(FAILED_TO_READ_TAGS_CACHE, exc_info=True)

    tags = [TagResponse.model_validate(tag) for tag in get_tags(db)]

    if cache is not None:
        try:
            cache.set(TAGS_CACHE_KEY, tags_adapter.dump_json(tags), ex=TAGS_CACHE_TTL)
        except RedisError:
            logger.warning(FAILED_TO_WRITE_TAGS_CACHE, exc_info=True)

    return tags
