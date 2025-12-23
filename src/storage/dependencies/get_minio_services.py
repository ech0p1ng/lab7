from config import settings
from storage.services.minio_service import MinioService


def get_minio_service() -> MinioService:
    return MinioService(
        settings.minio.bucket_name,
        settings.minio.endpoint,
        settings.minio.access_key,
        settings.minio.secret_key,
    )
