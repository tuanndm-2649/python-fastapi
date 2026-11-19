from sqlalchemy import Column, ForeignKey, Table, Uuid

from demo_fastapi.database import Base

task_tags = Table(
    "task_tags",
    Base.metadata,
    Column(
        "task_id",
        Uuid(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Uuid(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


task_bookmarks = Table(
    "task_bookmarks",
    Base.metadata,
    Column(
        "task_id",
        Uuid(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
