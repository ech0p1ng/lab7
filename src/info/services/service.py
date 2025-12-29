from info.schemas.schema import InfoSchema
from storage.services.minio_service import MinioService
from storage.services.service import StorageService
from analytics.services.service import AnalyticsService


class InfoService:
    def __init__(
        self,
        minio_service: MinioService,
        storage_service: StorageService,
        analytics_service: AnalyticsService
    ) -> None:
        self.minio_service = minio_service
        self.storage_service = storage_service
        self.analytics_service = analytics_service
        self.subject_area_file_name = 'temp/subject_area.txt'
        self.target_attribute_file_name = 'temp/target_attribute.txt'

    async def get_train_data(self, limit: int = 100, offset: int = 0) -> dict:
        df = (await self.analytics_service.load_csv(self.analytics_service.file_name))
        df_slice = df.iloc[offset:offset + limit + 1]
        return df_slice.to_dict()

    async def get_subject_area(self) -> str:
        subject_area_file_name = self.subject_area_file_name.split('/')[-1]
        await self.storage_service.download_file(
            self.minio_service.get_file_url_for_private(subject_area_file_name),
            self.subject_area_file_name
        )
        return await self.storage_service.read_file(self.subject_area_file_name)

    async def get_target_attribute(self) -> str:
        target_attribute_file_name = self.target_attribute_file_name.split('/')[-1]
        await self.storage_service.download_file(
            self.minio_service.get_file_url_for_private(target_attribute_file_name),
            self.target_attribute_file_name
        )
        return await self.storage_service.read_file(self.target_attribute_file_name)

    async def get_info(self) -> InfoSchema:
        return InfoSchema(
            train_data=await self.get_train_data(),
            subject_area=await self.get_subject_area(),
            target_attribute=await self.get_target_attribute()
        )
