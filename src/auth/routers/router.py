from fastapi import APIRouter, Depends
from dependencies.services import auth_service, user_service
from auth.services.service import AuthService
from user.services.service import UserService
from user.schemas.schema import UserSchema, UserSimpleSchema, UserAuthSchema, UserRegistrationSchema
from user.models.model import UserModel
from dependencies.auth import get_current_user
from auth.schemas.token import JwtToken
from logger import logger

router = APIRouter(prefix='/auth', tags=['Аутентификация'])


@router.post(
    path='/login',
    summary='Вход',
    description='Вход. Получение JWT-токена по данным пользователя',
    response_model=JwtToken
)
async def get_token(
    user_data: UserAuthSchema,
    auth_service: AuthService = Depends(auth_service),
    user_service: UserService = Depends(user_service)
):
    user = await user_service.get({'user_name': user_data.user_name})
    return await auth_service.get_token(user.id)


@router.post(
    path='/registration',
    summary='Регистрация',
    description='Регистрация',
    response_model=JwtToken
)
async def registration(
    user_data: UserRegistrationSchema,
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
