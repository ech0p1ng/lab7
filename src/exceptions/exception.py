from typing import Any
from fastapi import status


class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal server error"
    headers: dict[str, Any] | None = None

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class NotFoundError(AppException):
    '''
    Ошибка, которая выбрасывается в случае, если не удалось найти что-либо
    '''
    status_code = status.HTTP_404_NOT_FOUND


class AlreadyExistsError(AppException):
    '''
    Ошибка, которая выбрасывается в случае, если что-либо уже существует и не должно иметь дубликатов
    '''
    status_code = status.HTTP_400_BAD_REQUEST


class ForbiddenError(AppException):
    '''Ошибка, которая выбрасывается в случае, запрета доступа'''
    status_code = status.HTTP_403_FORBIDDEN


class WasNotCreatedError(AppException):
    '''
    Ошибка, которая выбрасывается в случае, если что-либо не было создано по какой-либо причине
    '''
    status_code = status.HTTP_400_BAD_REQUEST


class FileIsTooLargeError(AppException):
    '''
    Ошибка, которая выбрасывается в случае, если файл слишком большой
    '''
    status_code = status.HTTP_413_CONTENT_TOO_LARGE


class UnauthorizedError(AppException):
    '''
    Ошибка, которая выбрасывается в случае, если пользователь неавторизован
    '''
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}


class BadCredentialsError(AppException):
    '''
    Ошибка, которая выбрасывается в случае, если данные для авторизации невалидны
    '''
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}
