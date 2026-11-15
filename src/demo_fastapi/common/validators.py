from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from demo_fastapi.crud.projects import get_project
from demo_fastapi.crud.tags import get_tags_by_ids
from demo_fastapi.crud.users import get_user_profile_by_username, retrieve_user
from demo_fastapi.models import Project, Tag, User


def get_project_or_404(db: Session, project_id: UUID) -> Project:
    project = get_project(db, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


def get_user_or_404(db: Session, user_id: UUID) -> User:
    user = retrieve_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


def get_user_profile_or_404(db: Session, username: str) -> User:
    user = get_user_profile_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


def get_tags_or_404(db: Session, tag_ids: list[UUID]) -> list[Tag]:
    if not tag_ids:
        return []

    requested_ids = set(tag_ids)
    tags = get_tags_by_ids(db, list(requested_ids))
    missing_ids = requested_ids - {tag.id for tag in tags}

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found tag ids: {', '.join(sorted(str(tag_id) for tag_id in missing_ids))}",
        )

    return tags
