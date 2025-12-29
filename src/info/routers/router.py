from fastapi import APIRouter, Depends
from dependencies.services import info_service
from info.services.service import InfoService
from info.schemas.schema import InfoSchema


router = APIRouter(prefix='/info', tags=['Общая информация'])


@router.get(
    path="/",
    summary='Получение общей информации',
    description=('Получение общей информации. '
                 'Права доступа: студент, преподаватель, суперюзер'),
    response_model=InfoSchema
)
async def get_info(
    service: InfoService = Depends(info_service)
):
    return await service.get_info()


@router.get(
    path="/subject_area",
    summary='Получение информации о предметной области',
    description=('Получение информации о предметной области. '
                 'Права доступа: студент, преподаватель, суперюзер'),
    response_model=str
)
async def get_subject_area(
    service: InfoService = Depends(info_service)
):
    return await service.get_subject_area()


@router.get(
    path="/target_attribute",
    summary='Получение информации о предметной области',
    description=('Получение информации о предметной области. '
                 'Права доступа: студент, преподаватель, суперюзер'),
    response_model=str
)
async def get_target_attribute(
    service: InfoService = Depends(info_service)
):
    return await service.get_target_attribute()


@router.get(
    path="/train_data",
    summary='Получение информации о предметной области',
    description=('Получение информации о предметной области. '
                 'Права доступа: студент, преподаватель, суперюзер'),
    response_model=dict
)
async def get_train_data(
    limit: int = 100,
    offset: int = 100,
    service: InfoService = Depends(info_service)
):
    return await service.get_train_data(limit=limit, offset=offset)
