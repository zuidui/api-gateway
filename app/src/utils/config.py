import os
import secrets

from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


class Settings(BaseSettings):
    DEV: bool
    DEBUG: bool
    DOCKERHUB_USERNAME: str
    AUTHOR: str
    LICENSE: str
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

    @property
    def TEAM_SERVICE_URL(self):
        return f"http://{self.TEAM_SERVICE_HOST}:{self.TEAM_SERVICE_PORT}{self.API_PREFIX}/graphql"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings():
    return Settings()
