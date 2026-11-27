from uuid import UUID

from demo_fastapi.constants.user import UserRole
from demo_fastapi.models import User


def is_admin_or_owner(user: User, owner_id: UUID) -> bool:
    return user.role == UserRole.ADMIN or user.id == owner_id
