from enum import StrEnum


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


TASK_TITLE_MAX_LENGTH = 200
TASK_TITLE_MIN_LENGTH = 1
