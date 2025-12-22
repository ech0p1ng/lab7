from config import settings
from storage.services.minio_service import MinioService

minio_client = MinioService


def get_minio_service() -> MinioService:
    return MinioService(
        settings.minio.minio_bucket_name,
        settings.minio.minio_endpoint,
        settings.minio.minio_access_key,
        settings.minio.minio_secret_key,
    )
