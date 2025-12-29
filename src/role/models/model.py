from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from base.model import BaseModel
from role.schemas.schema import RoleSchema, RoleSimpleSchema
from endpoint.models.model import EndpointModel

if TYPE_CHECKING:
    from user.models.model import UserModel


class RoleModel(BaseModel):
    '''
    Роль

    Args:
        id (int): Идентификатор
        role_name (str): Название роли

    '''
    __tablename__ = 'role'
    role_name: Mapped[str]
    users: Mapped[list['UserModel']] = relationship(
        back_populates='role',
        lazy='selectin',
    )

    endpoints: Mapped[list['EndpointModel']] = relationship(
        back_populates='roles',
        uselist=True,
        secondary='permission',
        lazy='selectin'
    )

    @classmethod
    def from_schema(cls, schema: RoleSchema | RoleSimpleSchema) -> 'RoleModel':
        if type(schema) is RoleSchema:
            return cls(
                id=schema.id,
                role_name=schema.role_name
            )
        else:
            return cls(
                role_name=schema.role_name
            )
