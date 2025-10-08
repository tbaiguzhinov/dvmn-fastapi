import logging

import anyio
from gotenberg_api import GotenbergServerError
from html_page_generator import AsyncPageGenerator

from gotenberg_service import GotenbergService
from minio_service import MinioService

logger = logging.getLogger(__name__)


async def generate_page(
    user_prompt: str,
    minio_service: MinioService,
    gotenberg_service: GotenbergService,
    debug: bool = False,
):
    generator = AsyncPageGenerator()
    with anyio.CancelScope(shield=True):
        async for chunk in generator(user_prompt):
            if debug:
                print(chunk, end="", flush=True)
            yield chunk
        await minio_service.upload_file(generator.html_page.html_code, file_name="index.html", content_type='text/html')

        try:
            screenshot = await gotenberg_service.generate_image(generator.html_page.html_code.encode())
        except GotenbergServerError as e:
            logger.error(e)
            screenshot = None
        await minio_service.upload_file(screenshot, file_name="index.png", content_type="image/png")
