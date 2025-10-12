import logging

import httpx
from gotenberg_api import ScreenshotHTMLRequest

from env_settings import settings

logger = logging.getLogger(__name__)


class GotenbergService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.width = settings.gotenberg.width
        self.format = settings.gotenberg.format
        self.wait_delay = settings.gotenberg.wait_delay

    async def generate_image(self, raw_html: str):
        screenshot_bytes = await ScreenshotHTMLRequest(
            index_html=raw_html,
            width=self.width,
            format=self.format,
            wait_delay=self.wait_delay,
        ).asend(self.client)
        return screenshot_bytes
