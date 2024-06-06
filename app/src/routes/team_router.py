from fastapi import APIRouter, HTTPException, status

from resolver.team_schema import TeamInput
from resolver.player_schema import PlayerInput

from service.team_service import create_team_via_graphql, create_player_via_graphql

from utils.logger import logger_config

log = logger_config(__name__)
team_router = APIRouter()


@team_router.post("/team/create", response_model=TeamInput, tags=["Team"])
async def create_team(request: TeamInput):
    log.info(f"Creating team with data: {request}")
    team_created = await create_team_via_graphql(request)
    if team_created:
        log.info(f"Team created: {team_created}")
        return team_created
    log.error("Failed to create team")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Team not created"
    )


@team_router.post("/team/player/create", response_model=PlayerInput, tags=["Player"])
async def create_player(request: PlayerInput):
    log.info(f"Creating player with data: {request}")
    player_created = await create_player_via_graphql(request)
    if player_created:
        log.info(f"Player created: {player_created}")
        return player_created
    log.error("Failed to create player")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Player not created"
    )
