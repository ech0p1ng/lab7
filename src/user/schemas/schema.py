from pydantic import Field
from base.schema import BaseSimpleSchema
from role.schemas.schema import RoleSchema


class UserSimpleSchema(BaseSimpleSchema):
    '''
    Упрощенаня pydantic-модель пользователя

    Args:
        id (int): Telegram id (не @username) пользователя
        first_name (str): Имя
        last_name (str): Фамилия
        middle_name (str): Отчество
        role_id (int): Идентификатор роли
    '''
    id: int = Field(gt=0)
    first_name: str = Field(min_length=2, max_length=32)
    last_name: str = Field(min_length=1, max_length=32)
    middle_name: str = Field(min_length=5, max_length=32)
    role_id: int = Field(gt=0)


class UserSchema(BaseSimpleSchema):
    '''
    Pydantic-модель пользователя

    Args:
        id (int): Telegram id (не @username) пользователя
        first_name (str): Имя
        last_name (str): Фамилия
        middle_name (str): Отчество
        role (RoleSchema): Роль
    '''
    id: int = Field(gt=0)
    first_name: str = Field(min_length=2, max_length=32)
    last_name: str = Field(min_length=1, max_length=32)
    middle_name: str = Field(min_length=5, max_length=32)
    role: RoleSchema
