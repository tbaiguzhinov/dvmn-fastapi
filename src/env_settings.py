from enum import Enum

from pydantic import HttpUrl, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeepSeekSettings(BaseSettings):
    api_key: SecretStr
    max_connections: PositiveInt | None = None


class UnsplashSettings(BaseSettings):
    api_key: SecretStr
    max_connections: PositiveInt | None = None
    timeout: PositiveInt | None = None


class MinioSettings(BaseSettings):
    api_endpoint: HttpUrl
    login: str
    password: SecretStr
    bucket: str
    connection_timeout: PositiveInt | None = 10
    read_timeout: PositiveInt | None = 30
    max_pool_connections: PositiveInt | None = 50


class FormatEnum(str, Enum):
    JPEG = 'jpeg'
    PNG = 'png'
    WEBP = 'webp'


class GotenbergSettings(BaseSettings):
    base_url: HttpUrl
    width: int = 1000
    format: FormatEnum = FormatEnum.JPEG
    wait_delay: int = 8
    timeout: int = 20
    max_connections: int = 5


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    app_name: str = "My App"
    debug: bool = False

    deepseek: DeepSeekSettings
    unsplash: UnsplashSettings
    minio: MinioSettings
    gotenberg: GotenbergSettings


settings = AppSettings()
