import uvicorn
import debugpy  # type: ignore

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import logger_config
from utils.config import get_settings

from routes.team_router import team_router
from routes.health_router import health_router
from routes.graphql_router import graphql_app

log = logger_config(__name__)
settings = get_settings()

def start_debug_server():
    log.info("Starting debug server...")
    debugpy.listen((settings.APP_HOST, settings.DEBUG_PORT))
    log.info("Debug server started")
    debugpy.wait_for_client()

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
    log.info(f"Frontend service URL: {settings.FRONTEND_SERVICE_URL}")
    log.info(f"Team service URL: {settings.TEAM_SERVICE_URL}")

    app = FastAPI(
        title=settings.IMAGE_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.IMAGE_VERSION,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=settings.DOC_URL,
    )

    app.add_middleware(
        CORSMiddleware,
        # Need to check how to allow only the API Gateway URL and the Database URI
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(graphql_app(), prefix=settings.API_PREFIX)
    app.include_router(team_router, prefix=settings.API_PREFIX)

    log.info("Application created successfully")

    if settings.DEBUG: 
        start_debug_server()

    return app

app = init_app()

if __name__ == "__main__":
    log.info("Starting application...")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
    log.info("Application started")
