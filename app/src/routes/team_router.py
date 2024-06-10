from typing import Optional
from fastapi import APIRouter, HTTPException, status

from resolver.team_schema import TeamCreateRequest, TeamCreateResponse

from service.team_service import TeamService

from utils.logger import logger_config

log = logger_config(__name__)
team_router = APIRouter()


@team_router.post("/team/create", response_model=TeamCreateRequest, tags=["Team"])
async def create_team(request: TeamCreateRequest) -> Optional[TeamCreateResponse]:
    log.info(f"Creating team with data: {request}")
    team_created = await TeamService.create_team_via_graphql(request)
    if team_created:
        log.info(f"Team created: {team_created}")
        return team_created
    log.error("Failed to create team")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Team not created"
    )
