from typing import Optional
from fastapi import APIRouter

from resolver.team_schema import (
    TeamDataInput,
    TeamDataType,
)

from resolver.player_schema import (
    PlayerDataType,
    PlayerDataInput,
)

from service.gateway_service import GatewayService

from exceptions.gateway_exceptions import (
    PlayerCreationError,
    TeamCreationError,
    TeamJoinError,
)

from utils.logger import logger_config

log = logger_config(__name__)
app_router = APIRouter()


@app_router.post("/team/create", response_model=TeamDataType, tags=["Team"])
async def create_team(request: TeamDataInput) -> Optional[TeamDataType]:
    log.info(f"Creating team with data: {request}")
    try:
        team_created = await GatewayService.create_team_via_graphql(request)
        if team_created:
            log.info(f"Team created: {team_created}")
            return team_created
    except TeamCreationError as e:
        raise e
    return None


@app_router.post("/team/player/create", response_model=PlayerDataType, tags=["Team"])
async def create_player(request: PlayerDataInput) -> Optional[PlayerDataType]:
    log.info(f"Creating player with data: {request}")
    try:
        player_created = await GatewayService.create_player_via_graphql(request)
        if player_created:
            log.info(f"Player created: {player_created}")
            return player_created
    except PlayerCreationError as e:
        raise e
    return None


@app_router.post("/team/join", response_model=TeamDataType, tags=["Team"])
async def join_team(request: TeamDataInput) -> Optional[TeamDataType]:
    log.info(f"Joining team with data: {request}")
    try:
        team_joined = await GatewayService.join_team_via_graphql(request)
        if team_joined:
            log.info(f"Team joined: {team_joined}")
            return team_joined
    except TeamJoinError as e:
        raise e
    return None
