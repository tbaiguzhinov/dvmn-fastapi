import anyio
from html_page_generator import AsyncPageGenerator

from minio_service import MinioService


async def generate_page(user_prompt: str):
    generator = AsyncPageGenerator()
    minio_service = MinioService()
    with anyio.CancelScope(shield=True):
        async for chunk in generator(user_prompt):
            print(chunk, end="", flush=True)
            yield chunk
        await minio_service.upload_file(generator.html_page.html_code, file_name="index.html")
