import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient

from env_settings import settings
from gotenberg_service import GotenbergService
from minio_service import MinioService
from routers.sites_router import sites_router
from routers.user_router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализируем сервисы один раз при старте приложения
    app.state.minio_service = MinioService()
    app.state.gotenberg_service = GotenbergService()

    async with (
        AsyncUnsplashClient.setup(
            settings.unsplash.api_key.get_secret_value(),
            timeout=3,
        ),
        AsyncDeepseekClient.setup(
            settings.deepseek.api_key.get_secret_value(),
        ),
    ):
        yield


app = FastAPI(root_path="/frontend-api", lifespan=lifespan)

app.include_router(user_router)
app.include_router(sites_router)


def mount_if_exists(path, directory, name, html=False):
    if os.path.exists(directory):
        app.mount(path, StaticFiles(directory=directory, html=html), name=name)


mount_if_exists("/generated", "generated", "generated")
mount_if_exists("/", "frontend", "site", html=True)
mount_if_exists("/assets", "frontend/assets", "assets")
