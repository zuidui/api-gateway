import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import logger_config
from utils.config import get_settings

from routes.user import user_router
from routes.health import health_router
from routes.graphql import graphql_app

log = logger_config(__name__)
settings = get_settings()


def init_app():
    log.info("Creating application...")
    log.info(f"Image: {settings.IMAGE_NAME}:{settings.IMAGE_VERSION}")
    log.info(f"Author: {settings.AUTHOR}")
    log.info(f"License: {settings.LICENSE}")
    log.info(f"Application module: {settings.APP_MODULE}")
    log.info(f"Application port: {settings.APP_PORT}")
    log.info(f"Application host: {settings.APP_HOST}")
    log.info(f"Application description: {settings.APP_DESCRIPTION}")
    log.info(f"API prefix: {settings.API_PREFIX}")
    log.info(f"Documentation URL: {settings.DOC_URL}")
    log.info(f"User service URL: {settings.USER_SERVICE_URL}")

    app = FastAPI(
        title=settings.IMAGE_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.IMAGE_VERSION,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=settings.DOC_URL,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8080",
            "http://localhost:8081",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(graphql_app(), prefix=settings.API_PREFIX)
    app.include_router(user_router, prefix=settings.API_PREFIX)

    log.info("Application created successfully")

    return app


app = init_app()

if __name__ == "__main__":
    log.info("Starting application...")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
    log.info("Application started")
