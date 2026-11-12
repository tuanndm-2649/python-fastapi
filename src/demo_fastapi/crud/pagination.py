from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from demo_fastapi.models.pagination import PaginationParams


def paginate[T](
    db: Session,
    statement: Select[T],
    pagination: PaginationParams,
) -> tuple[list[T], int]:
    count_statement = select(func.count()).select_from(
        statement.order_by(None).subquery()
    )

    total = db.execute(count_statement).scalar_one()

    paginated_statement = statement.offset(pagination.offset).limit(
        pagination.page_size
    )

    items = list(db.scalars(paginated_statement).all())

    return items, total
