from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from base.model import BaseModel
from user.schemas.schema import UserSchema, UserSimpleSchema, UserAuthSchema
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from role.models.model import RoleModel


class UserModel(BaseModel):
    '''
    SQL Alchemy модель пользователя

    Args:
        id (int): Идентификатор
        user_name (str): Имя
        password (str): Пароль
        role (RoleModel): Роль
        groups (list[GroupModel]): группы, в которых состоит пользователь
        themes (list[ThemeModel]): темы, автором которых является пользователь
    '''
    __tablename__ = 'user'
    id: Mapped[int]
    user_name: Mapped[str]  # имя
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
    role: Mapped['RoleModel'] = relationship(
        back_populates='users',
        lazy='selectin',
    )

    @classmethod
    def from_schema(
        cls,
        schema: UserSchema | UserSimpleSchema | UserAuthSchema
    ) -> 'UserModel':
        from role.models.model import RoleModel
        if type(schema) is UserSchema:
            return cls(
                id=schema.id,
                user_name=schema.user_name,
                password=schema.password,
                role=RoleModel.from_schema(schema.role),
            )
        elif type(schema) is UserSimpleSchema:
            return cls(
                id=schema.id,
                user_name=schema.user_name,
                password=schema.password,
                role_id=schema.role_id,
            )
        elif type(schema) is UserAuthSchema:
            return cls(
                user_name=schema.user_name,
                password=schema.password,
            )
        else:
            return cls()
