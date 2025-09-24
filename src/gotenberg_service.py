import logging

import httpx
from gotenberg_api import GotenbergServerError, ScreenshotHTMLRequest

from env_settings import settings

logger = logging.getLogger(__name__)


class GotenbergService:
    def __init__(self):
        self.base_url = settings.gt.base_url
        self.timeout = settings.gt.timeout
        self.width = settings.gt.width
        self.format = settings.gt.format
        self.wait_delay = settings.gt.wait_delay
        self.max_connections = settings.gt.max_connections

    async def generate_image(self, raw_html: str):
        try:
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
        except GotenbergServerError as e:
            logger.error(e)
            screenshot_bytes = None
        return screenshot_bytes
