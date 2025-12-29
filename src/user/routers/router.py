from fastapi import APIRouter, Depends
from dependencies.permissions import check_permission
from dependencies.auth import get_current_user
from exceptions.exception import ForbiddenError
from user.schemas.schema import UserSimpleSchema, UserSchema
from user.models.model import UserModel
from user.services.service import UserService
from dependencies.services import user_service


router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.post(
    path="/",
    summary='Создание пользователя',
    description=('Cоздание пользователя. '
                 'Права доступа: преподаватель, суперюзер'),
    response_model=UserSchema
)
async def add_user(
    user_data: UserSimpleSchema,
    service: UserService = Depends(user_service)
):
    return await service.create(UserModel.from_schema(user_data))


@router.get(
    path="/",
    summary='Получение списка пользователей',
    description=('Получение списка пользователей. '
                 'Права доступа: студент, преподаватель, суперюзер'),
    response_model=list[UserSchema]
)
async def get_users(service: UserService = Depends(user_service)):
    all_models = await service.get_all()

    return [UserSchema.model_validate(model) for model in all_models]


@router.patch(
    path="/",
    summary='Обновление пользователя',
    description=('Обновление пользователя. '
                 'Права доступа: ученик, преподаватель, суперюзер'),
    response_model=UserSchema
)
async def update_user(
    user_data: UserSchema,
    service: UserService = Depends(user_service),
    current_user: UserModel = Depends(get_current_user),
    permission_allowed: bool = Depends(check_permission(
        endpoint_name='api_users_patch',
    ))
):
    if current_user.id == user_data.id:
        return await service.update(
            UserModel.from_schema(user_data),
            {"id": user_data.id}
        )
    else:
        raise ForbiddenError()


@router.delete(
    path="/",
    summary='Удаление пользователя',
    description=('Удаление пользователя. '
                 'Права доступа: суперюзер'),
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(user_service),
    current_user: UserModel = Depends(get_current_user),
    permission_allowed: bool = Depends(check_permission(
        endpoint_name='api_users_delete',
    ))
) -> None:
    if current_user.id == user_id:
        return await service.delete({"id": user_id})
    else:
        raise ForbiddenError()


@router.get(
    path='/me',
    summary='Получить данные о себе',
    description='Получить данные о себе',
    response_model=UserSchema
)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get(
    path='/{user_id}',
    summary='Получение пользователя',
    description=('Получение пользователя. '
                 'Права доступа: студент, преподаватель, суперюзер'),
    response_model=UserSchema
)
async def get_user(
    user_id: int,
    service: UserService = Depends(user_service)
):
    return await service.get({"id": user_id})
