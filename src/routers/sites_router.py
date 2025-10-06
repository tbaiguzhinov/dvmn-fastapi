from fastapi import APIRouter, Body, Path
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
def get_my_sites():
    endpoint = settings.mn.api_endpoint
    bucket = settings.mn.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}/{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}/{bucket}/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": f"{endpoint}/{bucket}/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return MySitesResponse(sites=[data])


@sites_router.post("/create", response_model=SiteCreateResponse, summary='Создать сайт')
def create_site(request: SiteCreateRequest):
    endpoint = settings.mn.api_endpoint
    bucket = settings.mn.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}/{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}/{bucket}/index.html",
        "id": 1,
        "prompt": request.prompt,
        "screenshotUrl": f"{endpoint}/{bucket}/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return data


@sites_router.post(
    "/{site_id}/generate",
    summary='Сгенерировать HTML код сайта',
    description='Код сайта будет транслироваться стримом по мере генерации.',
)
async def generate_site(site_id: int = Path(..., gt=0), request: SiteGenerationRequest = Body(...)):
    return StreamingResponse(
        content=generate_page(user_prompt=request.prompt, debug=settings.debug),
        media_type="text/plain",
    )


@sites_router.get("/{site_id}", response_model=SiteCreateResponse, summary='Получить сайт')
def get_site(site_id: int = Path(..., gt=0)):
    endpoint = settings.mn.api_endpoint
    bucket = settings.mn.bucket
    data = {
        "createdAt": "2025-06-15T18:29:56+00:00",
        "htmlCodeDownloadUrl": f"{endpoint}/{bucket}/index.html?response-content-disposition=attachment",
        "htmlCodeUrl": f"{endpoint}/{bucket}/index.html",
        "id": 1,
        "prompt": "Сайт любителей играть в домино",
        "screenshotUrl": f"{endpoint}/{bucket}/index.png",
        "title": "Фан клуб Домино",
        "updatedAt": "2025-06-15T18:29:56+00:00",
    }
    return data
