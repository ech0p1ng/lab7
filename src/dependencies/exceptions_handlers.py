import json
from typing import Any
from fastapi import FastAPI, HTTPException, Request, status, Response
from fastapi.responses import JSONResponse
from exceptions.exception import AppException
from starlette.exceptions import HTTPException as StarletteHTTPException


def set_exceptions_handlers(app: FastAPI) -> FastAPI:
    def generate_response(detail: str, status_code: int, headers: dict[str, Any] | None = None) -> Response:
        return JSONResponse(
            content={
                'status_code': status_code,
                'detail': [{
                    'msg': detail
                }],
            },
            status_code=status_code,
            headers=headers
        )

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException
    ) -> Response:
        return generate_response(
            detail=exc.detail,
            status_code=exc.status_code,
            headers=exc.headers
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):
        return generate_response(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        return generate_response(
            status_code=exc.status_code,
            detail=exc.detail,
            headers=exc.headers,  # type:ignore
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exception: Exception
    ) -> Response:
        # if isinstance(exception, FastAPIError):
        #     raise exception
        return generate_response(
            detail='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return app
