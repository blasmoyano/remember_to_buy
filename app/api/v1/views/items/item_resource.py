
from fastapi import status, Depends, APIRouter, Path

from app.api.v1.schemas.item_schema import ItemSchema, ItemFilter, ItemUpdate
from app.api.v1.schemas.response_schema import CommonResponse
from app.api.v1.models.items_model import ItemModel
from app.api.v1.depends.depends import get_pagination_query, PaginationQuery, get_db
from app.api.v1.middlewares.after_route import AfterRoute
from sqlalchemy.orm import Session
from app.database import crud

router = APIRouter(route_class=AfterRoute)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=CommonResponse[ItemSchema],
)
async def get_items(
    pagination: PaginationQuery = Depends(get_pagination_query),
    db: Session = Depends(get_db),
):
    """
    Get all items
    """

    item, meta = crud.get_all(model=ItemModel, db=db, per_page=pagination.per_page, page=pagination.page)
    return CommonResponse(response=item, meta=meta)


@router.post(
    "",
    response_model=CommonResponse[ItemSchema],
    status_code=status.HTTP_201_CREATED,
)
async def post_component(
        obj: ItemSchema,
        db: Session = Depends(get_db),
):
    """
    Post item
    """
    model_obj = ItemModel(**obj.dict())
    result = crud.add(db=db, obj=model_obj)

    return CommonResponse(response=ItemSchema.from_orm(result).dict())

@router.get(
    "/{creator}", response_model=CommonResponse[ItemSchema], status_code=status.HTTP_200_OK
)
async def get_item(
    creator: str,
    filters: ItemFilter = Depends(ItemFilter),
    db: Session = Depends(get_db)
):
    """
    Get items by category
    """

    filters = filters.dict()
    filters['creator'] = creator
    result = crud.get_items(db=db, model=ItemModel, filters=filters)

    return CommonResponse(response=result)




@router.delete(
    "/{id}", response_model=CommonResponse[ItemSchema], status_code=status.HTTP_200_OK
)
async def delete_type(
    id: int = Path(description="id_item"),
    db: Session = Depends(get_db)
):
    """
    Delete item by id
    """
    result = crud.delete_by_id(db=db, model=ItemModel, id_obj=id)
    return CommonResponse(response=result)


@router.put(
    "/{id}", response_model=CommonResponse[ItemSchema], status_code=status.HTTP_200_OK
)
async def put_type(
    obj: ItemUpdate,
    id: int = Path(description="id_item"),
    db: Session = Depends(get_db)
):
    """
    Put items by id
    """

    put_dict = obj.dict()

    put_dict["id"] = id

    result = crud.update(db=db, model=ItemModel, data=put_dict)
    return CommonResponse(response=result)