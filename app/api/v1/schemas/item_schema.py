from typing import Optional

from pydantic import BaseModel, Field, validator
from app.api.v1.models.items_model import Category

class ItemSchema(BaseModel):
    id: Optional[int]
    category: Category = Category.compact_disc
    title: str
    creator: str
    creator_label: str
    i_have_it: bool = False

    @validator('creator')
    def transform(cls, v):
        return v.lower()

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

class ItemUpdate(BaseModel):
    i_have_it: bool = False

class ItemFilter(BaseModel):
    category: Category = Category.compact_disc
    i_have_it: bool = Field(alias="lo_tengo")