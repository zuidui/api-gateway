from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils.logger import logger_config

log = logger_config(__name__)


class BaseServiceError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class TeamCreationError(BaseServiceError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


class PlayerCreationError(BaseServiceError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


class RatingCreationError(BaseServiceError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


class TeamJoinError(BaseServiceError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


app = FastAPI()


@app.exception_handler(TeamCreationError)
async def team_creation_exception_handler(request: Request, exc: TeamCreationError):
    log.error(f"Team creation error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(PlayerCreationError)
async def player_creation_exception_handler(request: Request, exc: PlayerCreationError):
    log.error(f"Player creation error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(RatingCreationError)
async def rating_creation_exception_handler(request: Request, exc: RatingCreationError):
    log.error(f"Rating creation error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(TeamJoinError)
async def team_join_exception_handler(request: Request, exc: TeamJoinError):
    log.error(f"Team join error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
