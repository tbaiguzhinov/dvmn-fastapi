import logging

import aioboto3
import anyio
from gotenberg_api import GotenbergServerError
from html_page_generator import AsyncPageGenerator
from httpx import AsyncClient

from gotenberg_service import generate_image
from minio_service import upload_file

logger = logging.getLogger(__name__)


async def generate_page(
    user_prompt: str,
    minio_client: aioboto3.Session.client,
    gotenberg_client: AsyncClient,
    debug: bool = False,
):
    generator = AsyncPageGenerator()
    with anyio.CancelScope(shield=True):
        async for chunk in generator(user_prompt):
            if debug:
                print(chunk, end="", flush=True)
            yield chunk
        await upload_file(minio_client, generator.html_page.html_code, file_name="index.html", content_type='text/html')

        try:
            screenshot = await generate_image(gotenberg_client, generator.html_page.html_code.encode())
        except GotenbergServerError as e:
            logger.error(e)
            screenshot = None
        await upload_file(minio_client, screenshot, file_name="index.png", content_type="image/png")
