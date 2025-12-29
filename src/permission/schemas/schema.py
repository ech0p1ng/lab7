from pydantic import Field
from base.schema import BaseSimpleSchema, BaseSchema


class PermissionSimpleSchema(BaseSimpleSchema):
    '''
    Pydantic-схема ограничения доступа

    Args:
        role_id (int): Идентификатор роли, которой доступна ручка
        endpoint_id (int): Идентификатор ручки
    '''
    role_id: int = Field(gt=0)
    endpoint_id: int = Field(gt=0)


class PermissionSchema(BaseSchema, PermissionSimpleSchema):
    '''
    Pydantic-схема ограничения доступа

    Args:
        role_id (int): Идентификатор роли, которой доступна ручка
        endpoint_id (int): Идентификатор ручки
    '''
