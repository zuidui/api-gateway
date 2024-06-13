import os
import secrets

from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


class Settings(BaseSettings):
    DEBUG: bool
    DEBUG_PORT: int
    LOG_LEVEL: str
    DOCKERHUB_USERNAME: str
    IMAGE_NAME: str
    IMAGE_VERSION: str
    APP_MODULE: str
    APP_PORT: int
    APP_HOST: str
    APP_DESCRIPTION: str
    API_PREFIX: str
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    DOC_URL: str
    DEPENDENCIES: str
    TEAM_SERVICE_HOST: str
    TEAM_SERVICE_PORT: int
    FRONTEND_SERVICE_HOST: str
    FRONTEND_SERVICE_PORT: int
    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int
    RATING_SERVICE_HOST: str
    RATING_SERVICE_PORT: int

    @property
    def RATING_SERVICE_URL(self):
        return f"http://{self.RATING_SERVICE_HOST}:{self.RATING_SERVICE_PORT}{self.API_PREFIX}/graphql"

    @property
    def TEAM_SERVICE_URL(self):
        return f"http://{self.TEAM_SERVICE_HOST}:{self.TEAM_SERVICE_PORT}{self.API_PREFIX}/graphql"

    @property
    def FRONTEND_SERVICE_URL(self):
        return f"http://{self.FRONTEND_SERVICE_HOST}:{self.FRONTEND_SERVICE_PORT}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings():
    return Settings()
