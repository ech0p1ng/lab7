from base.service import BaseService
from endpoint.models.model import EndpointModel
from endpoint.repositories.repository import EndpointRepository
from sqlalchemy.ext.asyncio import AsyncSession
from endpoint.schemas.endpoint import EndpointSimpleSchema


class EndpointService(BaseService[EndpointModel]):
    '''
    Бизнес-логика ручек
    '''

    def __init__(self, db: AsyncSession):
        '''
        Бизнес логика ручек

        Args:
            db (AsyncSession): Асинхронная сессия БД
        '''
        super().__init__(
            EndpointRepository(db),
            EndpointModel,
            single_model_name="ручка",
            multiple_models_name="ручки"
        )

    async def create(self, model: EndpointModel) -> EndpointModel:
        '''
        Создание ручки

        Args:
            model (PermissionModel): SQLAlchemy-модель ручки

        Returns:
            PermissionModel: SQLAlchemy-модель ручки

        Raises:
            WasNotCreatedError: Ручка не была создана
        '''
        filter = {"name": model.name}
        if not await self.exists(filter, raise_exc=False):
            return await super().create(model)
        else:
            return await self.get(filter)

    async def create_with_name(self, endpoint_name: str) -> EndpointModel:
        '''
        Создание ручки

        Args:
            endpoint_name (str): Имя ручки

        Returns:
            PermissionModel: SQLAlchemy-модель ручки

        Raises:
            WasNotCreatedError: Ручка не была создана
        '''

        model = EndpointModel.from_schema(
            EndpointSimpleSchema(
                name=endpoint_name
            )
        )
        return await self.create(model)
