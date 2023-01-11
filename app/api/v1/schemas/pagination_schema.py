from typing import Optional

from pydantic import BaseModel


class PaginationQuery(BaseModel):
    page: Optional[int]
    per_page: Optional[int]
