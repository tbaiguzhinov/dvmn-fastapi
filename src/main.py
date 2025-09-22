from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import APIRouter, Body, FastAPI, Path
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from html_page_generator import AsyncDeepseekClient, AsyncUnsplashClient
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from env_settings import settings
from page_generator import generate_page


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

user_router = APIRouter(prefix="/users", tags=['users'])
sites_router = APIRouter(prefix="/sites", tags=['sites'])


class UserModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    email: str
    is_active: bool
    profile_id: int
    registered_at: datetime
    updated_at: datetime
    username: str


class SiteCreateRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "google": {
                "prompt": "Сайт любителей играть в домино",
                "title": "Фан клуб игры в домино",
            },
        },
    )
    title: str | None = None
    prompt: str


class SiteGenerationRequest(BaseModel):
    prompt: str | None = None


class SiteCreateResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
    created_at: datetime
    html_code_download_url: str
    html_code_url: str
    id: int
    prompt: str
    screenshot_url: str
    title: str
    updated_at: datetime


class MySitesResponse(BaseModel):
    sites: list[SiteCreateResponse]


@user_router.get("/me", response_model=UserModel)
async def get_user_info():
    data = {
        "email": "google@google.com",
        "isActive": True,
        "profileId": "1",
        "registeredAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return data


@sites_router.post("/create", response_model=SiteCreateResponse)
def create_site(request: SiteCreateRequest):
    endpoint = settings.mn.api_endpoint
    bucket = settings.mn.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}/{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}/{bucket}/index.html",
        "id": 1,
        "prompt": request.prompt,
        "screenshotUrl": "http://google.com/media/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return data


@sites_router.post("/{site_id}/generate")
async def generate_site(site_id: int = Path(..., gt=0), request: SiteGenerationRequest = Body(...)):
    return StreamingResponse(
        content=generate_page(user_prompt=request.prompt),
        media_type="text/plain",
    )


@sites_router.get("/my", response_model=MySitesResponse)
def get_my_sites():
    endpoint = settings.mn.api_endpoint
    bucket = settings.mn.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}/{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}/{bucket}/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": "http://google.com/media/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return MySitesResponse(sites=[data])


@sites_router.get("/{site_id}", response_model=SiteCreateResponse)
def get_site(site_id: int = Path(..., gt=0)):
    endpoint = settings.mn.api_endpoint
    bucket = settings.mn.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}/{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}/{bucket}/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": "http://google.com/media/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return data


app.include_router(user_router)
app.include_router(sites_router)

app.mount("/generated", StaticFiles(directory="generated"), name="generated")
app.mount("/", StaticFiles(directory="frontend", html=True), name="site")
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
