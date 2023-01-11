from app.api.v1.views.items import item_resource
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(item_resource.router, prefix="/items", tags=["items"])
