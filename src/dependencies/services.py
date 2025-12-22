from fastapi import Depends
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from attachment.services.service import AttachmentService
from role.services.service import RoleService
from auth.services.service import AuthService
from endpoint.services.service import EndpointService
from permission.services.service import PermissionService
from user.services.service import UserService
from storage.services.minio_service import MinioService
from config import settings


def user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    '''
    Получить объект класса бизнес-логики пользователя

    Args:
        db (AsyncSession): Асинхронная сессия БД

    Returns:
        UserService: Объект класса бизнес-логики пользователя
    '''
    return UserService(db)


def attachment_service(
        db: AsyncSession = Depends(get_db)
) -> AttachmentService:
    '''
    Получить объект класса бизнес-логики прикрепляемого медиа-контента

    Args:
        db (AsyncSession): Асинхронная сессия БД

    Returns:
        AttachmentService: Объект класса бизнес-логики \
            прикрепляемого медиа-контента
    '''
    return AttachmentService(
        db,
        minio_service()
    )


def role_service(
    db: AsyncSession = Depends(get_db)
) -> RoleService:
    '''
    Получить объект класса бизнес-логики роли

    Args:
        db (AsyncSession): Асинхронная сессия БД

    Returns:
        AttachmentService: Объект класса бизнес-логики роли
    '''
    return RoleService(db)


def auth_service(
    db: AsyncSession = Depends(get_db)
) -> AuthService:
    '''
    Получить объект класса бизнес-логики аутентификации

    Args:
        db (AsyncSession): Асинхронная сессия БД

    Returns:
        AttachmentService: Объект класса бизнес-логики аутентификации
    '''
    return AuthService(user_service(db))


def minio_service() -> MinioService:
    '''
    Получить сервис MinIO

    Returns:
        MinioService: Cервис MinIO
    '''

    return MinioService(
        bucket_name=settings.minio.minio_bucket_name,
        endpoint=settings.minio.minio_endpoint,
        access_key=settings.minio.minio_access_key,
        secret_key=settings.minio.minio_secret_key
    )


def endpoint_service(
    db: AsyncSession = Depends(get_db)
) -> EndpointService:
    '''
    Получить объект класса бизнес-логики ручек

    Args:
        db (AsyncSession): Асинхронная сессия БД

    Returns:
        EndpointService: Объект класса бизнес-логики ручек
    '''
    return EndpointService(db)


def permission_service(
    db: AsyncSession = Depends(get_db)
) -> PermissionService:
    '''
    Получить объект класса бизнес-логики ограничения \
        доступа к ручкам по ролям

    Args:
        db (AsyncSession): Асинхронная сессия БД

    Returns:
        PermissionService: Объект класса бизнес-логики ограничения \
        доступа к ручкам по ролям
    '''
    return PermissionService(
        db,
        endpoint_service(db),
        role_service(db)
    )
