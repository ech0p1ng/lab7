from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from base.model import BaseModel
from user.schemas.schema import UserSchema, UserSimpleSchema
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from role.models.model import RoleModel


class UserModel(BaseModel):
    '''
    SQL Alchemy модель пользователя

    Args:
        id (int): Идентификатор
        first_name (str): Имя
        last_name (str): Фамилия
        middle_name (str): Отчество
        role (RoleModel): Роль
        groups (list[GroupModel]): группы, в которых состоит пользователь
        themes (list[ThemeModel]): темы, автором которых является пользователь
    '''
    __tablename__ = 'user'
    id: Mapped[int]
    first_name: Mapped[str]  # имя
    last_name: Mapped[str]  # фамилия
    middle_name: Mapped[str]  # отчество

    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
    role: Mapped['RoleModel'] = relationship(
        back_populates='users',
        lazy='selectin',
    )

    @classmethod
    def from_schema(
        cls,
        schema: UserSchema | UserSimpleSchema
    ) -> 'UserModel':
        from role.models.model import RoleModel
        if type(schema) is UserSchema:
            return cls(
                id=schema.id,
                first_name=schema.first_name,
                last_name=schema.last_name,
                middle_name=schema.middle_name,
                role=RoleModel.from_schema(schema.role),
            )
        elif type(schema) is UserSimpleSchema:
            return cls(
                id=schema.id,
                first_name=schema.first_name,
                last_name=schema.last_name,
                middle_name=schema.middle_name,
                role_id=schema.role_id
            )
        else:
            return cls()
