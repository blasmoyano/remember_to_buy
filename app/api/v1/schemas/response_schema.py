from typing import List
from typing import Optional, Union, Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class Error(BaseModel):
    description: str
    status_code: Optional[int] = None
    exception: Optional[str] = None
    details: Optional[dict] = None

    @staticmethod
    def from_exception(
        exception: Exception,
        status_code: Optional[int] = None,
        description: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        return Error(
            description=description or str(exception),
            status_code=status_code,
            exception=type(exception).__name__,
            details={} if details is None else details,
        )


class Meta(BaseModel):
    page: int
    total_items: int
    per_page: int
    total_pages: int
    previous: int
    next: int


T = TypeVar("T")


class CommonResponse(GenericModel, Generic[T]):
    response: Optional[Union[T, List[T]]]
    errors: Optional[List[Error]] = []
    meta: Optional[Meta]
