import os

from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


class Settings(BaseSettings):
    DEBUG: bool
    DEBUG_PORT: str
    LOG_LEVEL: str
    DOCKERHUB_USERNAME: str
    IMAGE_NAME: str
    IMAGE_VERSION: str
    APP_MODULE: str
    APP_PORT: str
    APP_HOST: str
    APP_DESCRIPTION: str
    API_PREFIX: str
    DOC_URL: str
    DEPENDENCIES: str
    TEAM_SERVICE_HOST: str
    TEAM_SERVICE_PORT: str
    FRONTEND_SERVICE_HOST: str
    FRONTEND_SERVICE_PORT: str
    RATING_SERVICE_HOST: str
    RATING_SERVICE_PORT: str

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
