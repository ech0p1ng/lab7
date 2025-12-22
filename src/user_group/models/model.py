from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from base.model import BaseModel


class UserGroupModel(BaseModel):
    '''Таблица для разрыва связи "многие ко многим"
    у таблиц group и user'''
    __tablename__ = 'user_group'
    group_id: Mapped[int] = mapped_column(ForeignKey('group.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
