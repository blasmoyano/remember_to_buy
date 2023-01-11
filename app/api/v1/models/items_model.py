
from enum import Enum
import sqlalchemy as db

from app.database.database import Base


class Category(str, Enum):
    compact_disc: str = "cd"
    vinyl_disc: str = "vinilo"
    games: str = "juegos"
    supermarket: str = "lista"
    books: str = "libros"


class ItemModel(Base):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, index=True)
    category = db.Column(
        db.Enum(Category, name="category", default=Category.compact_disc),
        nullable=False,
    )
    title = db.Column(db.String, index=True)
    creator = db.Column(db.String, nullable=False)
    creator_label = db.Column(db.String, nullable=False)
    i_have_it = db.Column(db.Boolean, unique=False, default=False)