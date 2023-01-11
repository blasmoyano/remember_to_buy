from fastapi import APIRouter

from app.api.v1 import api_router as router

api_router = APIRouter()
api_router.include_router(router=router, prefix="/v1.0")