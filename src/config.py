from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from typing import Self

dot_env_path = str(Path(__file__).parent.parent.parent / '.env')


class MinioSettings(BaseSettings):
    minio_access_key: str  # deprecated
    minio_secret_key: str  # deprecated
    minio_bucket_name: str
    minio_endpoint: str
    # minio_root_user: str
    # minio_root_password: str


class PostgresSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    db_dsn: str = ''
    db_dsn_sync: str = ''

    @model_validator(mode='after')
    def db_dsn_validate(self) -> Self:
        self.db_dsn = (f'postgresql+asyncpg://'
                       f'{self.postgres_user}:{self.postgres_password}@'
                       f'{self.postgres_host}:{self.postgres_port}/'
                       f'{self.postgres_db}')

        self.db_dsn_sync = (f'postgresql+psycopg://'
                            f'{self.postgres_user}:{self.postgres_password}@'
                            f'{self.postgres_host}:{self.postgres_port}/'
                            f'{self.postgres_db}')
        return self


class KeycloakSettings(BaseSettings):
    keycloak_base_url: str
    keycloak_admin: str
    keycloak_admin_password: str


class AttachmentsSettings(BaseSettings):
    attachments_max_size: int
    attachments_extensions: List[str]


class JwtSettings(BaseSettings):
    access_token_expire: int
    algorithm: str
    secret_key: str


class Settings(BaseSettings):

    # MinIO
    minio: MinioSettings

    # PostgreSQL
    postgres: PostgresSettings

    # Keycloak
    keycloak: KeycloakSettings

    # Attachments
    attachments: AttachmentsSettings

    # Jwt
    jwt: JwtSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file=dot_env_path,
        env_file_encoding='utf-8',
        extra='ignore')


settings = Settings()  # type: ignore
