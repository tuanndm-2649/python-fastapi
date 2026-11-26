"""Database operations for comments."""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from demo_fastapi.models import Comment, Task, User
from demo_fastapi.schemas.comments import CommentCreate, CommentUpdate


def create_comment(
    db: Session, payload: CommentCreate, task: Task, user: User
) -> Comment:
    comment = Comment(content=payload.content, task=task, author=user)

    try:
        db.add(comment)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment: Comment) -> None:
    try:
        db.delete(comment)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


def update_comment(db: Session, comment: Comment, payload: CommentUpdate) -> Comment:
    comment.content = payload.content

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(comment)
    return comment
