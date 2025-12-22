from fastapi import APIRouter, Depends
from dependencies.services import auth_service, user_service
from auth.services.service import AuthService
from auth.schemas.schema import AuthSchema
from user.services.service import UserService
from user.schemas.schema import UserSchema, UserSimpleSchema
from user.models.model import UserModel
from dependencies.auth import get_current_user


router = APIRouter(prefix='/auth', tags=['Аутентификация'])


@router.post(
    path='/login',
    summary='Вход',
    description='Вход. Получение JWT-токена по данным пользователя',
)
async def get_token(
    user_data: AuthSchema,
    auth_service: AuthService = Depends(auth_service)
):
    return await auth_service.get_token(user_data.id)


@router.get(
    path='/me',
    summary='Получить данные о себе',
    description='Получить данные о себе',
    response_model=UserSchema
)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.post(
    path='/registration',
    summary='Регистрация',
    description='Регистрация',
)
async def registration(
    user_data: UserSimpleSchema,
    user_service: UserService = Depends(user_service),
    auth_service: AuthService = Depends(auth_service)
):
    user = await user_service.create(UserModel.from_schema(user_data))
    return await auth_service.get_token(user.id)


@router.post(
    path='/refresh',
    summary='Обновление токена',
    description='Обновление токена'
)
async def token_refresh(
    user_data: UserSimpleSchema,
    auth_service: AuthService = Depends(auth_service)
):
    return await auth_service.get_token(user_data.id)
