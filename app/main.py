from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.api.v1.errors.error_handling import (
    validation_exception_handler,
    repository_exception_handler,
    service_exception_handler,
    request_validation_exception_handler,
    bad_request_exception_handler,
    unauthorized_exception_handler,
    forbidden_exception_handler,
    not_found_exception_handler,
    internal_server_error_exception_handler,
)
from app.api.v1.errors.errors import RepositoryError, ServiceError

from app.config.settings import settings

from app.api.v1 import models
from app.database.database import engine

# models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.API_NAME,
    description=f"{settings.DESCRIPTION}",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    contact={"name": "che_market", "email": "chemarket@protonmail.com"},
    exception_handlers={
        400: bad_request_exception_handler,
        401: unauthorized_exception_handler,
        403: forbidden_exception_handler,
        404: not_found_exception_handler,
        500: internal_server_error_exception_handler,
        ValidationError: validation_exception_handler,
        RepositoryError: repository_exception_handler,
        ServiceError: service_exception_handler,
        RequestValidationError: request_validation_exception_handler,
    },
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api")
