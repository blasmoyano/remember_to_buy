from typing import Optional
from typing import Generator
from fastapi import Query
import logging

from app.api.v1.schemas.pagination_schema import PaginationQuery

from app.database.database import SessionLocal
log = logging.getLogger("uvicorn")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except Exception:
        pass
    finally:
        db.close()
def get_pagination_query(
    page: Optional[int] = Query(1, title="page", ge=1),
    per_page: Optional[int] = Query(30, title="items for page", ge=1, le=9999),
) -> PaginationQuery:
    return PaginationQuery(page=page, per_page=per_page)

