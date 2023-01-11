from sqlalchemy.orm import Session
from typing import TypeVar, List
from app.api.v1.models import items_model
from app.api.v1.helpers import generate_meta
from app.api.v1.errors.errors import RepositoryError
T = TypeVar("T")


def get_items(db: Session, model, filters):

    return db.query(model).filter(
        model.category == filters['category'].value,
        model.creator == filters['creator'],
        model.i_have_it == filters['i_have_it']
    ).all()


def get_all(model, page, per_page, db: Session):
    try:
        total = db.query(model).count()
        meta = generate_meta(page, per_page, total)
        data = (db.query(model).limit(per_page).offset(page - 1).all())
    except Exception as e:
        raise RepositoryError(repr(e))

    return data, meta


def add(db: Session, obj: T) -> T:
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
    except Exception as e:
        raise RepositoryError(repr(e))
    return obj


def get_by_id(db: Session, id_obj, model) -> List[T]:
    obj = db.query(model).get(id_obj)
    if obj is None:
        raise RepositoryError(
            [f"{model.__name__} not found with id {id_obj}"]
        )
    return obj

def delete_by_id(db: Session, model, id_obj):
    obj = get_by_id(db=db, model=model, id_obj=id_obj)
    if obj is not None:
        db.delete(obj)
        db.commit()
    return obj

def update(db, model, data) -> T:
    obj = get_by_id(db=db, model=model, id_obj=data['id'])
    if obj is None:
        raise RepositoryError(
            [f"{model.__name__} not found with id {data['id']}"]
        )
    for key, value in data.items():
        setattr(obj, key, value)
    try:
        db.add(obj)
        db.commit()
    except Exception as e:
        raise RepositoryError(repr(e))

    return obj