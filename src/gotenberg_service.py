import logging

import httpx
from gotenberg_api import ScreenshotHTMLRequest

from env_settings import settings

logger = logging.getLogger(__name__)


class GotenbergService:
    def __init__(self):
        self.base_url = str(settings.gotenberg.base_url)
        self.timeout = settings.gotenberg.timeout
        self.width = settings.gotenberg.width
        self.format = settings.gotenberg.format
        self.wait_delay = settings.gotenberg.wait_delay
        self.max_connections = settings.gotenberg.max_connections

    async def generate_image(self, raw_html: str):
        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
        ) as client:
            screenshot_bytes = await ScreenshotHTMLRequest(
                index_html=raw_html,
                width=self.width,
                format=self.format,
                wait_delay=self.wait_delay,
            ).asend(client)
            return screenshot_bytes
