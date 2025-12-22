from fastapi import Depends
from permission.services.service import PermissionService
from dependencies.services import (
    endpoint_service, permission_service, role_service
)
from dependencies.auth import get_current_user
from role.services.service import RoleService
from endpoint.services.service import EndpointService
from user.models.model import UserModel
from exceptions.exception import UnauthorizedError, ForbiddenError


def check_permission(
    endpoint_name: str
):
    '''
    Зависимость для ограничения доступа к ручке по ролям

    Args:
        allowed_roles (list[int]): Список id ролей, \
            для которых доступна ручка
        endpoint_name (str): Имя ручки

    Raises:
        NotFoundError: Ручка не найдена по имени или роль не найдена
        UnauthorizedError: Пользователь неавторизован

    Returns:
        bool: Доступ запрещен/разрешен
    '''
    async def _permission_check(
        permission_service: PermissionService = Depends(permission_service),
        endpoint_service: EndpointService = Depends(endpoint_service),
        role_service: RoleService = Depends(role_service),
        current_user: UserModel = Depends(get_current_user)
    ):
        allow = False

        if current_user is None:
            raise UnauthorizedError('Вы неавторизованы')

        endpoint = await endpoint_service.get({
            "name": endpoint_name
        })

        permissions = await permission_service.get_multiple(
            {"endpoint_id": endpoint.id}
        )

        allowed_roles_ids = {permission.role_id for permission in permissions}

        for role_id in allowed_roles_ids:
            role = await role_service.get({"id": role_id})
            print(role.role_name)
            if current_user.role == role:
                allow = True
                break

        if not allow:
            raise ForbiddenError('Доступ запрещен')
        return allow
    return _permission_check
