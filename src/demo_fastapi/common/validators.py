from uuid import UUID

from sqlalchemy.orm import Session

from demo_fastapi.constants.message import TAGS_NOT_FOUND, USER_NOT_FOUND
from demo_fastapi.crud.tags import get_tags_by_ids
from demo_fastapi.crud.users import get_user_profile_by_username, retrieve_user
from demo_fastapi.exceptions import NotFoundException
from demo_fastapi.models import Tag, User


def get_user_detail(db: Session, user_id: UUID) -> User:
    user = retrieve_user(db, user_id)

    if user is None:
        raise NotFoundException(USER_NOT_FOUND)

    return user


def get_user_profile(db: Session, username: str) -> User:
    user = get_user_profile_by_username(db, username)

    if user is None:
        raise NotFoundException(USER_NOT_FOUND)

    return user


def get_task_tags(db: Session, tag_ids: list[UUID]) -> list[Tag]:
    if not tag_ids:
        return []

    requested_ids = set(tag_ids)
    tags = get_tags_by_ids(db, list(requested_ids))
    missing_ids = requested_ids - {tag.id for tag in tags}

    if missing_ids:
        missing_text = ", ".join(sorted(str(tag_id) for tag_id in missing_ids))
        raise NotFoundException(TAGS_NOT_FOUND.format(tag_ids=missing_text))

    return tags
