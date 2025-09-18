from pydantic import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeepSeekSettings(BaseSettings):
    api_key: SecretStr
    max_connections: PositiveInt | None = None


class UnsplashSettings(BaseSettings):
    api_key: SecretStr
    max_connections: PositiveInt | None = None
    timeout: PositiveInt | None = None


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    app_name: str = "My App"
    debug: bool = False

    ds: DeepSeekSettings
    us: UnsplashSettings


settings = AppSettings()
