from sqlalchemy import ForeignKey
from base.model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from permission.schemas.schema import (
    PermissionSchema, PermissionSimpleSchema
)


class PermissionModel(BaseModel):
    '''
    Таблица для разрыва связи "многие ко многим" \
    у таблиц endpoint и role
    '''
    __tablename__ = 'permission'
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
    endpoint_id: Mapped[int] = mapped_column(ForeignKey('endpoint.id'))

    @classmethod
    def from_schema(cls, schema: PermissionSimpleSchema | PermissionSchema):
        if type(schema) is PermissionSchema:
            return cls(
                id=schema.id,
                role_id=schema.role_id,
                endpoint_id=schema.endpoint_id
            )
        else:
            return cls(
                role_id=schema.role_id,
                endpoint_id=schema.endpoint_id
            )
