from pydantic import Field
from base.schema import BaseSimpleSchema
from role.schemas.schema import RoleSchema


class UserSimpleSchema(BaseSimpleSchema):
    '''
    Упрощенаня pydantic-модель пользователя

    Args:
        id (int): Telegram id (не @username) пользователя
        user_name (str): Имя
        role_id (int): Идентификатор роли
    '''
    id: int = Field(gt=0)
    user_name: str = Field(min_length=2, max_length=32)
    role_id: int = Field(gt=0)


class UserSchema(BaseSimpleSchema):
    '''
    Pydantic-модель пользователя

    Args:
        id (int): Id пользователя
        user_name (str): Имя
        role (RoleSchema): Роль
    '''
    id: int = Field(gt=0)
    user_name: str = Field(min_length=2, max_length=32)
    role: RoleSchema
