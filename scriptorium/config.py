from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_STRING_CONNECTION: str

    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str

    LOG_LEVEL: str = "ERROR"

    ENVIRONMENT: str = "development"


config = Settings()  # type: ignore
