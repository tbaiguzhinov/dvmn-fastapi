import asyncio
from datetime import datetime

import httpx
from fastapi import APIRouter, Body, FastAPI, Path
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

app = FastAPI(root_path="/frontend-api")

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
def get_user_info():
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
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": "http://google.com/media/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": "http://google.com/media/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": "http://google.com/media/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return data


async def site_generation_mock():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html")
            data = response.text

            chunk_size = 100
            chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

            for _, chunk in enumerate(chunks):
                await asyncio.sleep(0.1)
                yield chunk

    except Exception as e:
        yield f"error: {str(e)}\n\n"


@sites_router.post("/{site_id}/generate")
async def generate_site(site_id: int = Path(..., gt=0), request: SiteGenerationRequest = Body(...)):
    return StreamingResponse(
        content=site_generation_mock(),
        media_type="text/plain",
    )


@sites_router.get("/my", response_model=MySitesResponse)
def get_my_sites():
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": "http://google.com/media/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": "https://dvmn.org/media/filer_public/d1/4b/d14bb4e8-d8b4-49cb-928d-fd04ecae46da/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": "http://google.com/media/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return MySitesResponse(sites=[data])


@sites_router.get("/{site_id}", response_model=SiteCreateResponse)
def get_site(site_id: int = Path(..., gt=0)):
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": "http://google.com/media/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": "http://google.com/media/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": "http://google.com/media/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return data


app.include_router(user_router)
app.include_router(sites_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="site")

app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
