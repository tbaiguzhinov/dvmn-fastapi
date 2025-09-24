import anyio
from html_page_generator import AsyncPageGenerator

from gotenberg_service import GotenbergService
from minio_service import MinioService


async def generate_page(user_prompt: str, debug: bool = False):
    generator = AsyncPageGenerator()
    minio_service = MinioService()
    gotenberg_service = GotenbergService()
    with anyio.CancelScope(shield=True):
        async for chunk in generator(user_prompt):
            if debug:
                print(chunk, end="", flush=True)
            yield chunk
        await minio_service.upload_file(generator.html_page.html_code, file_name="index.html", content_type='text/html')
        screenshot = await gotenberg_service.generate_image(generator.html_page.html_code.encode())
        await minio_service.upload_file(screenshot, file_name="index.png", content_type="image/png")
