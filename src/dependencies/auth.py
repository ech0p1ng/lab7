from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from auth.services.service import AuthService, http_bearer
from dependencies.services import auth_service
from exceptions.exception import UnauthorizedError, NotFoundError
from user.models.model import UserModel


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: AuthService = Depends(auth_service),
) -> UserModel | None:
    '''
    Получить пользователя по его JWT-токену

    Args:
        token (str): JWT-токен
        auth_service (AuthService): Сервис аутентификации

    Returns:
        UserModel: Найденый пользователь, иначе `None`

    Raises:
        UnauthorizedError: Не удалось проверить учетные данные
    '''
    token = credentials.credentials
    try:
        user = await auth_service.get_user_by_token(token)
    except NotFoundError:
        raise UnauthorizedError("Вы неавторизованы")
    if type(user) is not UserModel:
        raise UnauthorizedError("Ожидался пользователь, а не tuple")
    return user


async def get_current_user_no_exc(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: AuthService = Depends(auth_service),
) -> UserModel | None:
    '''
    Получить пользователя по его JWT-токену без выбрасывания исключения

    Args:
        token (str): JWT-токен
        auth_service (AuthService): Сервис аутентификации

    Returns:
        UserModel: Найденый пользователь, иначе `None`
    '''
    try:
        token = credentials.credentials
        user = await auth_service.get_user_by_token(token)
        if not isinstance(user, UserModel):
            return None
        return user
    except (UnauthorizedError, NotFoundError):
        return None
