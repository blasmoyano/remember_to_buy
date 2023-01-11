from http.client import responses

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.v1.schemas.response_schema import Error, CommonResponse


async def bad_request_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_400_BAD_REQUEST)


async def unauthorized_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_401_UNAUTHORIZED)


async def forbidden_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_403_FORBIDDEN)


async def not_found_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_404_NOT_FOUND)


async def internal_server_error_exception_handler(
    request: Request, exc
) -> JSONResponse:
    return create_error_json_response(
        request, exc, status.HTTP_500_INTERNAL_SERVER_ERROR
    )


async def validation_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_404_NOT_FOUND)


async def repository_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_404_NOT_FOUND)


async def service_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_404_NOT_FOUND)


async def request_validation_exception_handler(request: Request, exc) -> JSONResponse:
    return create_error_json_response(request, exc, status.HTTP_404_NOT_FOUND)


def create_error_json_response(request: Request, exc: Exception, status_code: int):
    error = Error.from_exception(
        exc, status_code=status_code, description=str(exc) or responses[status_code]
    )

    return JSONResponse(
        status_code=status_code, content=jsonable_encoder(response_error(error))
    )


def response_error(error) -> dict:
    dict_error = CommonResponse(errors=[error]).dict(exclude_unset=True)
    dict_error["results"] = {}
    dict_error["_meta"] = {}
    return dict_error
