import os

import zipfile
import asyncio
import aiofiles
import aiohttp


class Client:

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def download_notes(self, url: str, number: str | int):
        while True:
            try:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(10)) as response:
                    if response.status == 200:
                        data = await response.read()
                        filename = f'/tmp/tmp_files0/{number}.xml'
                        async with aiofiles.open(filename, 'wb') as file:
                            await file.write(data)
                        return
                    else:
                        await asyncio.sleep(1)
            except (TimeoutError, aiohttp.ClientError):
                await asyncio.sleep(1)

    async def create_download_pool(
            self,
            data: dict,
            filename: str,
            concurrent_downloads: int = 30
    ):
        if not os.path.exists('/tmp/tmp_files0'):
            os.mkdir('/tmp/tmp_files0')

        try:
            semaphore = asyncio.Semaphore(concurrent_downloads)

            async def bounded_download(item):
                async with semaphore:
                    await self.download_notes(item['url'], item['identifier'])

            download_tasks = [asyncio.create_task(bounded_download(item)) for item in data['links']]

            await asyncio.gather(*download_tasks)

        finally:

            await self.create_zip(
                '/tmp/tmp_files0',
                filename)

    @staticmethod
    async def create_zip(path: str, filename: str):
        with zipfile.ZipFile(f'/tmp/{filename}', 'w', zipfile.ZIP_DEFLATED) as zipf:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_file() and entry.name.endswith('.xml'):
                        async with aiofiles.open(entry.path, 'rb') as file:
                            data = await file.read()
                        zipf.writestr(entry.name, data)
                        os.remove(entry.path)

    async def close_session(self):
        await self.session.close()
