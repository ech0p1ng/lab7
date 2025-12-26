from typing import Any
from fastapi import APIRouter, Depends
from role.models.model import RoleModel
from role.services.service import RoleService
from role.schemas.schema import RoleSimpleSchema, RoleSchema
from dependencies.services import role_service
from dependencies.permissions import check_permission


router = APIRouter(prefix='/roles', tags=['Роли'])


@router.get(
    path='/{role_id}',
    summary='Получение роли',
    description=('Получение роли. '
                 'Права доступа: все'),
    response_model=RoleSchema
)
async def get_role(
    role_id: int,
    service: RoleService = Depends(role_service)
) -> Any:
    return await service.get({"id": role_id})


@router.post(
    path="/",
    summary='Создание роли',
    description=('Cоздание роли. '
                 'Права доступа: суперюзер'),
    response_model=RoleSchema
)
async def add_role(
    role_data: RoleSimpleSchema,
    role_service: RoleService = Depends(role_service),
    # TODO: Подумать над пермишенами
    # permission_allowed: bool = Depends(check_permission(
    #     endpoint_name='api_roles_post',
    # ))
) -> Any:
    model = RoleModel.from_schema(role_data)
    created_model = await role_service.create(model)
    return RoleSchema.model_validate(created_model)


@router.get(
    path="/",
    summary='Получение списка ролей',
    description=('Получение списка ролей. '
                 'Права доступа: все'),
    response_model=list[RoleSchema]
)
async def get_roles(
    service: RoleService = Depends(role_service)
) -> Any:
    return await service.get_all()


@router.patch(
    path="/",
    summary='Обновление роли',
    description=('Обновление роли. '
                 'Права доступа: суперюзер'),
    response_model=RoleSchema
)
async def update_role(
    role_data: RoleSchema,
    service: RoleService = Depends(role_service),
    # TODO: Подумать над пермишенами
    # permission_allowed: bool = Depends(check_permission(
    #     endpoint_name='api_roles_patch',
    # ))
) -> Any:
    return await service.update(
        model=RoleModel.from_schema(role_data),
        filter={"id": role_data.id}
    )


@router.delete(
    path="/{role_id}",
    summary='Удаление роли',
    description=('Удаление роли. '
                 'Права доступа: суперюзер')
)
async def delete_role(
    role_id: int,
    service: RoleService = Depends(role_service),
    permission_allowed: bool = Depends(check_permission(
        endpoint_name='api_roles_delete',
    ))
) -> None:
    await service.delete({"id": role_id})
