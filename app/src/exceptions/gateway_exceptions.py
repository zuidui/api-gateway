from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from utils.logger import logger_config

log = logger_config(__name__)


class BaseServiceError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class TeamError(BaseServiceError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


class PlayerError(BaseServiceError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)


app = FastAPI()


@app.exception_handler(TeamError)
async def team_error_handler(request: Request, exc: TeamError):
    log.error(f"TeamError: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


@app.exception_handler(PlayerError)
async def player_error_handler(request: Request, exc: PlayerError):
    log.error(f"PlayerError: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
