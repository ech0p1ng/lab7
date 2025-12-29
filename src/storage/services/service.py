from pathlib import Path
import aiohttp
import aiofiles
from io import BytesIO


class StorageService:
    def __init__(self) -> None:
        pass

    def split_file_name(self, full_file_name: str) -> tuple[str, str]:
        '''
        Разделение полного имени файла на имя файла и его расширение

        Args:
            full_file_name (str): Полное имя файла с расширением

        Returns:
            tuple[str,str]: Первый объект - имя файла, \
                второй - расширение файла
        '''
        splitted = full_file_name.split(".")
        extension = splitted[-1]
        splitted.remove(extension)
        file_name = ".".join(splitted)
        return (file_name, extension)

    async def download_file(self, url: str, filename: str) -> None:
        '''
        Асинхронная загрузка файла

        Args:
            url (str): URL-файла
            filename (str): Имя файла
        '''
        file = Path(filename)
        parent = file.parent.absolute()
        parent.mkdir(parents=True, exist_ok=True)
        if file.exists():
            file.unlink(True)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                async with aiofiles.open(filename, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        await f.write(chunk)

    async def read_file(self, file_path: str, encoding="utf-8") -> str:
        async with aiofiles.open(file_path, "r", encoding=encoding) as f:
            return await f.read()

    async def read_file_as_bytes(self, file_path: str) -> BytesIO:
        async with aiofiles.open(file_path, "rb") as f:
            return BytesIO(await f.read())
