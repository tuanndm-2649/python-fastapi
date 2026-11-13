from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from demo_fastapi.schemas.pagination import PageResponse, PaginationParams


def paginate[T, S](
    db: Session,
    statement: Select[T],
    pagination: PaginationParams,
    response_type: type[PageResponse[S]],
) -> PageResponse[S]:
    count_statement = select(func.count()).select_from(
        statement.order_by(None).subquery()
    )

    total = db.execute(count_statement).scalar_one()

    paginated_statement = statement.offset(pagination.offset).limit(
        pagination.page_size
    )

    items = list(db.scalars(paginated_statement).all())

    return response_type.from_result(items, total, pagination)
