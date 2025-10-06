from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class SiteCreateRequest(BaseModel):
    title: str | None = None
    prompt: str

    model_config = ConfigDict(
        json_schema_extra={
            "google": {
                "prompt": "Сайт любителей играть в домино",
                "title": "Фан клуб игры в домино",
            },
            "examples": [
                {
                    "title": "Сайт любителей играть в домино",
                    "prompt": "Фан клуб игры в домино",
                },
            ],
        },
    )


class SiteGenerationRequest(BaseModel):
    prompt: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "prompt": "Фан клуб игры в домино",
                },
            ],
        },
    )


class SiteCreateResponse(BaseModel):
    created_at: datetime
    html_code_download_url: str
    html_code_url: str
    id: int
    prompt: str
    screenshot_url: str
    title: str
    updated_at: datetime

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "createdAt": "2025-06-15T18:29:56+00:00",
                    "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
                    "htmlCodeUrl": "http://example.com/media/index.html",
                    "id": 1,
                    "prompt": "Сайт любителей играть в домино",
                    "screenshotUrl": "http://example.com/media/index.png",
                    "title": "Фан клуб Домино",
                    "updatedAt": "2025-06-15T18:29:56+00:00",
                },
            ],
        },
    )


class MySitesResponse(BaseModel):
    sites: list[SiteCreateResponse]
