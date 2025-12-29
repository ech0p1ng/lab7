import ssl
import json
import uuid
import asyncio
from io import BytesIO
from minio import Minio
from config import settings
from datetime import timedelta
from minio.error import S3Error
from fastapi import File, UploadFile
from urllib3 import PoolManager, disable_warnings

from storage.services.service import StorageService
from attachment.schemas.schema import AttachmentMinioSchema
from exceptions.exception import FileIsTooLargeError, WasNotCreatedError


class MinioService:
    def __init__(
        self,
        bucket_name: str,
        endpoint: str,
        access_key: str,
        secret_key: str,
        storage_service: StorageService
    ):
        self.storage_service = storage_service

        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_SSLv3 | ssl.OP_NO_SSLv2

        disable_warnings()

        self._client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
            http_client=PoolManager(
                cert_reqs="CERT_NONE"
            )
        )

        self._bucket_name = bucket_name

        __policy = json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{self._bucket_name}/*"]
                    }
                ]
            }
        )
        self.client.set_bucket_policy(self._bucket_name, __policy)

    def __ensure_bucket_exists(self):
        '''
        Проверка существования MinIO Bucket. \
            В случае, если не существует, создает его

        Raises:
            S3Error: Ошибка MinIO
        '''
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise e

    async def upload_file(
        self,
        file: BytesIO,
        file_name: str,
        file_ext: str
    ) -> AttachmentMinioSchema:
        '''
        Загрузка файла в MinIO

        Args:
            file (BytesIO): Загружаемый файл
            file_name (str): Имя файла
            file_ext (str): Расширение файла без точки

        Returns:
            AttachmentMinioSchema: Упрощенная Pydantic-схема медиа-контента, \
            прикрепляемого к теме с URL файла в MinIO

        Raises:
            FileIsTooLargeError: Размер файла превышает допустимый
            WasNotCreatedError: Не удалось загрузить файл в MinIO
            Exception: Прочие ошибки, связаныне с MinIO
        '''
        self.__ensure_bucket_exists()

        try:
            full_file_name = f'{uuid.uuid4()}-{file_name}.{file_ext}'
            file.seek(0)
            file_size = file.getbuffer().nbytes

            public_url = self.get_file_url_for_public(full_file_name)
            private_url = self.get_file_url_for_private(full_file_name)

            if file_size > settings.attachment.max_size:
                raise FileIsTooLargeError(
                    "Максимальный размер файла - "
                    f"{settings.attachment.max_size / 1024} Кбайт"
                )
            else:
                await asyncio.to_thread(
                    self.client.put_object,
                    self.bucket_name,
                    full_file_name,
                    file,
                    file_size,
                    # content_type=str(file.content_type)
                )

                return AttachmentMinioSchema(
                    minio_public_file_url=public_url,
                    minio_private_file_url=private_url,
                    file_name=str(file_name),
                    file_extension=file_ext,
                    file_size=file_size
                )
        except S3Error as exc:
            raise WasNotCreatedError(str(exc))

    async def upload_file_from_form(
        self,
        file: UploadFile = File(...)
    ) -> AttachmentMinioSchema:
        '''
        Загрузка файла из запроса в MinIO

        Args:
            file (UploadFile): Загружаемый файл

        Returns:
            AttachmentMinioSchema: Упрощенная Pydantic-схема медиа-контента, \
            прикрепляемого к теме с URL файла в MinIO

        Raises:
            FileIsTooLargeError: Размер файла превышает допустимый
            WasNotCreatedError: Не удалось загрузить файл в MinIO
            Exception: Прочие ошибки, связаныне с MinIO
        '''
        full_file_name = file.filename or 'img.png'
        file_ext = full_file_name.split('.')[-1]
        file_name = full_file_name.replace(file_ext, '')
        __file = BytesIO(await file.read())
        return await self.upload_file(
            __file,
            file_name,
            file_ext
        )

    @property
    def client(self) -> Minio:
        return self._client

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    def get_file_url_for_private(self, file_name: str) -> str:
        '''
        Получение URL файла в MinIO

        Args:
            file_name (str): Полное имя файла

        Returns:
            str: URL файла в MinIO
        '''
        return f'http://{settings.minio.endpoint}/{settings.minio.bucket_name}/{file_name}'

    def get_file_url_for_public(self, file_name: str) -> str:
        return f'http://{settings.minio.ip_address}:{settings.minio.port}/{settings.minio.bucket_name}/{file_name}'
