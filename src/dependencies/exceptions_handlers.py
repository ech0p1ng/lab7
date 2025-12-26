import json
from typing import Any
from fastapi.exceptions import FastAPIError
from fastapi import FastAPI, HTTPException, Request, status, Response
from exceptions.exception import (
    NotFoundError, AlreadyExistsError, ForbiddenError, UnauthorizedError,
    WasNotCreatedError, FileIsTooLargeError, BadCredentialsError
)

def set_exceptions_handlers(app: FastAPI) -> FastAPI:
    def generate_response(detail: str, status_code: int, headers: dict[str, Any] | None = None) -> Response:
        return Response(
            content=str(json.dumps({
                'status_code': status_code,
                'detail': detail,
            })),
            status_code=status_code,
            headers=headers
        )

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(
        request: Request,
        exception: NotFoundError
    ) -> Response:
        return generate_response(
            detail=str(exception),
            status_code=status.HTTP_404_NOT_FOUND
        )

    @app.exception_handler(AlreadyExistsError)
    async def already_exists_error_handler(
        request: Request,
        exception: AlreadyExistsError
    ) -> Response:
        return generate_response(
            detail=str(exception),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    @app.exception_handler(ForbiddenError)
    async def forbidden_error_handler(
        request: Request,
        exception: ForbiddenError
    ) -> Response:
        return generate_response(
            detail=str(exception),
            status_code=status.HTTP_403_FORBIDDEN
        )

    @app.exception_handler(WasNotCreatedError)
    async def was_not_created_error_handler(
        request: Request,
        exception: WasNotCreatedError
    ) -> Response:
        return generate_response(
            detail=str(exception),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    @app.exception_handler(FileIsTooLargeError)
    async def file_is_too_large_error_handler(
        request: Request,
        exception: FileIsTooLargeError
    ) -> Response:
        return generate_response(
            detail=str(exception),
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        )

    @app.exception_handler(BadCredentialsError)
    async def bad_credentials_error_handler(
        request: Request,
        exception: BadCredentialsError
    ) -> Response:
        return generate_response(
            detail=str(exception),
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_error_handler(
        request: Request,
        exception: UnauthorizedError
    ) -> Response:
        return generate_response(
            detail=str(exception),
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={'WWW-Authenticate': 'Bearer'}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exception: Exception
    ) -> Response:
        if isinstance(exception, FastAPIError):
            raise exception
        return generate_response(
            detail='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return app
