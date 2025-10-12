import os
from contextlib import asynccontextmanager

import aioboto3
from aiobotocore.config import AioConfig
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from httpx import AsyncClient, Limits

from env_settings import settings
from gotenberg_service import GotenbergService
from minio_service import MinioService
from routers.sites_router import sites_router
from routers.user_router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    s3_config = AioConfig(
        max_pool_connections=settings.minio.max_pool_connections,
        connect_timeout=settings.minio.connection_timeout,
        read_timeout=settings.minio.read_timeout,
    )
    s3_session = aioboto3.Session()

    app.state.minio_client = s3_session.client(
        service_name='s3',
        endpoint_url=str(settings.minio.api_endpoint),
        aws_access_key_id=settings.minio.login,
        aws_secret_access_key=settings.minio.password.get_secret_value(),
        region_name='us-east-1',
        config=s3_config,
    )
    app.state.minio_service = MinioService(app.state.minio_client)

    httpx_gotenberg_client = AsyncClient(
        base_url=str(settings.gotenberg.base_url),
        timeout=settings.gotenberg.timeout,
        limits=Limits(max_connections=settings.gotenberg.max_connections),
    )
    app.state.gotenberg_service = GotenbergService(httpx_gotenberg_client)

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
