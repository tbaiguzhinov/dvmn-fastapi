from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient

from env_settings import settings
from src.routers.sites_router import sites_router
from src.routers.user_router import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with (
        AsyncUnsplashClient.setup(
            settings.us.api_key.get_secret_value(),
            timeout=3,
        ),
        AsyncDeepseekClient.setup(
            settings.ds.api_key.get_secret_value(),
        ),
    ):
        yield


app = FastAPI(root_path="/frontend-api", lifespan=lifespan)

app.include_router(user_router)
app.include_router(sites_router)

app.mount("/generated", StaticFiles(directory="generated"), name="generated")
app.mount("/", StaticFiles(directory="frontend", html=True), name="site")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
