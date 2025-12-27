from fastapi import APIRouter, Depends
from analytics.services.service import AnalyticsService
from dependencies.services import analytics_service

router = APIRouter(prefix='/analytics', tags=['Аналитика'])


@router.get(
    path="/",
    summary='Получение аналитики',
    description=('Получение аналитики. '),
)
async def get_users(service: AnalyticsService = Depends(analytics_service)):
    return await service.analyze()
