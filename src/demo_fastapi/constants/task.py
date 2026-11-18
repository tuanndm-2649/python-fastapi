from enum import StrEnum


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


TASK_TITLE_MAX_LENGTH = 200
TASK_TITLE_MIN_LENGTH = 1
