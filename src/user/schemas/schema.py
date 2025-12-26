from pydantic import Field
from base.schema import BaseSimpleSchema, BaseSchema
from role.schemas.schema import RoleSchema


class UserAuthSchema(BaseSimpleSchema):
    '''
    Pydantic-модель авторизации пользователя

    Args:
        user_name (str): Имя
        password (str): Пароль
    '''
    user_name: str = Field(min_length=2, max_length=32)
    password: str = Field(min_length=8, max_length=32)


class UserSimpleSchema(BaseSchema, UserAuthSchema):
    '''
    Упрощенаня pydantic-модель пользователя

    Args:
        id (int): Id пользователя
        user_name (str): Имя
        password (str): Пароль
        role_id (int): Идентификатор роли
    '''
    role_id: int = Field(gt=0)


class UserSchema(BaseSchema, UserAuthSchema):
    '''
    Pydantic-модель пользователя

    Args:
        id (int): Id пользователя
        user_name (str): Имя
        password (str): Пароль
        role (RoleSchema): Роль
    '''
    id: int = Field(gt=0)
    user_name: str = Field(min_length=2, max_length=32)
    role: RoleSchema
