from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


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
