from typing import Optional
from fastapi import APIRouter

from resolver.team_schema import TeamCreateRequest, TeamCreateResponse

from service.team_service import TeamService

from exceptions.team_exceptions import TeamCreationError

from utils.logger import logger_config

log = logger_config(__name__)
team_router = APIRouter()


@team_router.post("/team/create", response_model=TeamCreateResponse, tags=["Team"])
async def create_team(request: TeamCreateRequest) -> Optional[TeamCreateResponse]:
    log.info(f"Creating team with data: {request}")
    try:
        team_created = await TeamService.create_team_via_graphql(request)
        if team_created:
            log.info(f"Team created: {team_created}")
            return team_created
    except TeamCreationError as e:
        raise e
    return None
