from gotenberg_api import ScreenshotHTMLRequest

from env_settings import settings


async def generate_image(gotenberg_client, raw_html: str):
    screenshot_bytes = await ScreenshotHTMLRequest(
        index_html=raw_html,
        width=settings.gotenberg.width,
        format=settings.gotenberg.format,
        wait_delay=settings.gotenberg.wait_delay,
    ).asend(gotenberg_client)
    return screenshot_bytes
