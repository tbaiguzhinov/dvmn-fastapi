from fastapi import APIRouter, Body, Path, Request
from fastapi.responses import StreamingResponse

from env_settings import settings
from models.sites_models import MySitesResponse, SiteCreateRequest, SiteCreateResponse, SiteGenerationRequest
from page_generator import generate_page

sites_router = APIRouter(prefix="/sites", tags=['sites'])


@sites_router.get(
    "/my",
    response_model=MySitesResponse,
    summary='Получить список сгенерированных сайтов текущего пользователя',
)
def get_my_sites() -> MySitesResponse:
    endpoint = settings.minio.api_endpoint
    bucket = settings.minio.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}{bucket}/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": f"{endpoint}{bucket}/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return MySitesResponse(sites=[SiteCreateResponse(**data)])


@sites_router.post("/create", response_model=SiteCreateResponse, summary='Создать сайт')
def create_site(request: SiteCreateRequest) -> SiteCreateResponse:
    endpoint = settings.minio.api_endpoint
    bucket = settings.minio.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}{bucket}/index.html",
        "id": 1,
        "prompt": request.prompt,
        "screenshotUrl": f"{endpoint}{bucket}/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return SiteCreateResponse(**data)


@sites_router.post(
    "/{site_id}/generate",
    summary='Сгенерировать HTML код сайта',
    description='Код сайта будет транслироваться стримом по мере генерации.',
)
async def generate_site(
    request_obj: Request,
    site_id: int = Path(..., gt=0),
    request: SiteGenerationRequest = Body(...),
) -> StreamingResponse:
    return StreamingResponse(
        content=generate_page(
            user_prompt=request.prompt,
            minio_service=request_obj.app.state.minio_service,
            gotenberg_service=request_obj.app.state.gotenberg_service,
            debug=settings.debug,
        ),
        media_type="text/plain",
    )


@sites_router.get("/{site_id}", response_model=SiteCreateResponse, summary='Получить сайт')
def get_site(site_id: int = Path(..., gt=0)) -> SiteCreateResponse:
    endpoint = settings.minio.api_endpoint
    bucket = settings.minio.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}{bucket}/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": f"{endpoint}{bucket}/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return SiteCreateResponse(**data)
