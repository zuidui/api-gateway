import asyncio
from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import logger_config
from utils.config import get_settings

from events.consumer import Consumer, start_consumer

from routes.gateway_router import app_router
from routes.health_router import health_router
from routes.graphql_router import graphql_app, graphql_router

log = logger_config(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    consumer: Consumer = await start_consumer(loop, app)
    app.state.consumer = consumer
    try:
        yield
    finally:
        await consumer.close()


def init_app():
    log.info("Starting application...")
    log.info(f"Image: {settings.IMAGE_NAME}:{settings.IMAGE_VERSION}")
    log.info(f"Author: {settings.DOCKERHUB_USERNAME}")
    log.info(f"Application module: {settings.APP_MODULE}")
    log.info(f"Application port: {settings.APP_PORT}")
    log.info(f"Application host: {settings.APP_HOST}")
    log.info(f"Application description: {settings.APP_DESCRIPTION}")
    log.info(f"Debug mode: {settings.DEBUG}")
    log.info(f"Debug port: {settings.DEBUG_PORT}")
    log.info(f"API prefix: {settings.API_PREFIX}")
    log.info(
        f"Service API: http://{settings.IMAGE_NAME}:{settings.APP_PORT}{settings.API_PREFIX}"
    )
    log.info(
        f"Service documentation: http://{settings.IMAGE_NAME}:{settings.APP_PORT}{settings.DOC_URL}"
    )
    log.info(
        f"Service health-check: http://{settings.IMAGE_NAME}:{settings.APP_PORT}/health"
    )
    log.info(f"Service schema: http://{settings.IMAGE_NAME}:{settings.APP_PORT}/schema")
    log.info(f"Frontend service URL: {settings.FRONTEND_SERVICE_URL}")
    log.info(f"Team service URL: {settings.TEAM_SERVICE_URL}")
    log.info(f"Rating service URL: {settings.RATING_SERVICE_URL}")
    log.info(f"Broker: {settings.BROKER_URL}")
    log.info(f"Queue name: {settings.QUEUE_NAME}")
    log.info(f"Exchange name: {settings.EXCHANGE_NAME}")

    app = FastAPI(
        title=settings.IMAGE_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.IMAGE_VERSION,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=settings.DOC_URL,
        lifespan=lifespan,
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(graphql_router)
    app.include_router(graphql_app(), prefix=settings.API_PREFIX)
    app.include_router(app_router, prefix=settings.API_PREFIX)

    log.info("Application started successfully")

    return app


app = init_app()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
