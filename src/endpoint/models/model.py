from base.model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from endpoint.schemas.endpoint import EndpointSchema, EndpointSimpleSchema
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from role.models.model import RoleModel


class EndpointModel(BaseModel):
    __tablename__ = 'endpoint'
    name: Mapped[str] = mapped_column(nullable=False)

    roles: Mapped[list['RoleModel']] = relationship(
        back_populates='endpoints',
        uselist=True,
        secondary='permission',
        lazy='selectin'
    )

    @classmethod
    def from_schema(cls, schema: EndpointSimpleSchema | EndpointSchema):
        if type(schema) is EndpointSchema:
            return cls(
                id=schema.id,
                name=schema.name
            )
        else:
            return cls(
                name=schema.name
            )
