from sqlalchemy.ext.asyncio import AsyncSession
from permission.repositories.repository import PermissionRepository
from base.service import BaseService
from permission.models.model import PermissionModel
from permission.schemas.schema import PermissionSimpleSchema
from endpoint.services.service import EndpointService
from role.services.service import RoleService
from role.models.model import RoleModel
from endpoint.models.model import EndpointModel
from exceptions.exception import (
    ForbiddenError, NotFoundError, UnauthorizedError
)
from user.models.model import UserModel


class PermissionService(BaseService[PermissionModel]):
    '''
    Бизнес-логика ограничения доступа к ручкам по ролям
    '''

    def __init__(
        self, db: AsyncSession,
        endpoint_service: EndpointService,
        role_service: RoleService
    ):
        '''
        Бизнес-логика ограничения доступа к ручкам по ролям

        Args:
            db (AsyncSession): Асинхронная сессия БД
            endpoint_service (EndpointService): Сервис ручек
            role_service (RoleService): Сервис ролей
        '''
        self.endpoint_service = endpoint_service
        self.role_service = role_service
        super().__init__(
            PermissionRepository(db),
            PermissionModel,
            single_model_name="ограничение доступа к ручке по ролям",
            multiple_models_name="ограничения доступа к ручке по ролям"
        )

    async def create(self, model: PermissionModel) -> PermissionModel:
        '''
        Создание ограничения доступа к ручке по ролям

        Args:
            model (PermissionModel): SQLAlchemy-модель ограничения \
                доступа к ручке по ролям

        Returns:
            PermissionModel: SQLAlchemy-модель ограничения доступа \
                к ручке по ролям

        Raises:
            WasNotCreatedError: Ограничение доступа к ручке \
                по ролям не было создано
        '''
        filter = {
            "endpoint_id": model.endpoint_id,
            "role_id": model.role_id
        }
        if not await self.exists(filter, raise_exc=False):
            return await super().create(model)
        else:
            return await self.get(filter)

    async def create_with_role_and_endpoint(
        self,
        endpoint_model: EndpointModel,
        role_model: RoleModel
    ) -> PermissionModel:
        '''
        Создание ограничения доступа к ручке по ролям

        Args:
            endpoint_model (EndpointModel): SQLAlchemy-модель ручки
            role_model (RoleModel): SQLAlchemy-модель роли

        Returns:
            PermissionModel: SQLAlchemy-модель ограничения доступа \
                к ручке по ролям

        Raises:
            WasNotCreatedError: Ограничение доступа к ручке \
                по ролям не было создано
            NotFoundError: Ручка или роль не найдены
        '''
        await self.role_service.exists({
            "id": role_model.id,
            "role_name": role_model.role_name
        })
        await self.endpoint_service.exists({
            "id": endpoint_model.id,
            "name": endpoint_model.name
        })

        model = PermissionModel.from_schema(
            PermissionSimpleSchema(
                role_id=role_model.id,
                endpoint_id=endpoint_model.id
            )
        )

        permission = await self.create(model)
        return permission

    async def create_for_roles(
        self,
        endpoint_name: str,
        *role_models: RoleModel,
        create_endpoint: bool = True
    ) -> list[PermissionModel]:
        '''
        Создание ограничения доступа к ручке по нескольким ролям

        Args:
            endpoint_model (EndpointModel): SQLAlchemy-модель ручки
            *role_models (RoleModel): SQLAlchemy-модели ролей

        Returns:
            PermissionModel: SQLAlchemy-модель ограничения доступа \
                к ручке по ролям

        Raises:
            WasNotCreatedError: Ограничение доступа к ручке \
                по ролям не было создано
            NotFoundError: Роль не найдена
        '''
        endpoint_exists = self.endpoint_service.exists(
            {"name": endpoint_name},
            raise_exc=False
        )
        if endpoint_exists:
            endpoint = await self.endpoint_service.get(
                {"name": endpoint_name}
            )
        elif create_endpoint:
            endpoint = await self.endpoint_service.create_with_name(
                endpoint_name
            )
        else:
            raise NotFoundError('Ручка не найдена')

        permissions = []
        for role in role_models:
            filter = {
                "role_id": role.id,
                "endpoint_id": endpoint.id
            }
            if not await self.exists(filter, raise_exc=False):
                permission = await self.create_with_role_and_endpoint(
                    endpoint, role
                )
            else:
                permission = await self.get(filter)
            permissions.append(permission)

        return permissions

    async def check_permission(
        self,
        endpoint_name: str,
        user_model: UserModel,
        raise_exc: bool = True
    ) -> bool:
        '''
        Проверка доступа к ручке для пользователя

        Args:
            endpoint_name (str): Название ручки
            user_model (UserModel): SQLAlchemy-модель роли

        Returns:
            bool: `True` - доступ есть, `False` - доступа нет

        Raises:
            WasNotCreatedError: Ограничение доступа к ручке \
                по ролям не было создано
            ForbiddenError: Доступ запрещен
            NotFoundError: Ручка не найдена
        '''
        endpoint: EndpointModel = await self.endpoint_service.get({
            "name": endpoint_name
        })
        if user_model is None:
            raise UnauthorizedError("Вы неавторизованы")

        filter = {
            "endpoint_id": endpoint.id,
            "role_id": user_model.role.id
        }
        exists = await self.exists(filter, raise_exc=False)
        if raise_exc and not exists:
            raise ForbiddenError('Доступ запрещен')
        else:
            return exists
