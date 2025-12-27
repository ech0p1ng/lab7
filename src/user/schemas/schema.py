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

class UserRegistrationSchema(UserAuthSchema):
    '''
    Pydantic-модель регистрации пользователя

    Args:
        user_name (str): Имя
        password (str): Пароль
        role_id (int): ID роли пользователя
    '''
    role_id: int = Field(gt=0)


class UserSimpleSchema(BaseSchema, UserRegistrationSchema):
    '''
    Упрощенаня pydantic-модель пользователя

    Args:
        id (int): Id пользователя
        user_name (str): Имя
        password (str): Пароль
        role_id (int): Идентификатор роли
    '''
    pass

class UserSchema(BaseSchema, UserAuthSchema):
    '''
    Pydantic-модель пользователя

    Args:
        id (int): Id пользователя
        user_name (str): Имя
        password (str): Пароль
        role (RoleSchema): Роль
    '''
    role: RoleSchema
