import asyncio
from fastapi import APIRouter, HTTPException

from models.team_model import (
    TeamData,
    TeamDetails,
    TeamDataInput,
)

from models.player_model import (
    PlayerDataInput,
)

from service.gateway_service import GatewayService

from exceptions.gateway_exceptions import (
    TeamError,
    PlayerError,
)

from utils.logger import logger_config

log = logger_config(__name__)
app_router = APIRouter()


@app_router.post("/team/create", response_model=TeamData, tags=["Team"])
async def create_team(request: TeamDataInput) -> TeamData:
    log.info(f"Creating team with data: {request}")
    try:
        wait_event = asyncio.create_task(GatewayService.wait_for_event("team_created"))
        team_created = await GatewayService.create_team(request)
        if team_created:
            log.info(
                f"Team created: {team_created} - waiting for message from RabbitMQ"
            )
            message = await wait_event
            if message:
                return message
            else:
                raise HTTPException(
                    status_code=504, detail="No message received from RabbitMQ"
                )
    except TeamError as e:
        raise e
    raise HTTPException(status_code=500, detail="Failed to create team")


@app_router.post("/team/player/create", response_model=TeamDetails, tags=["Team"])
async def create_player(request: PlayerDataInput) -> TeamDetails:
    log.info(f"Creating player with data: {request}")
    try:
        wait_event = asyncio.create_task(
            GatewayService.wait_for_event("rating_updated")
        )
        player_created = await GatewayService.create_player(request)
        if player_created:
            message = await wait_event
            if message:
                return await GatewayService.get_players_data(request)
            else:
                raise HTTPException(
                    status_code=504, detail="No message received from RabbitMQ"
                )
    except PlayerError as e:
        raise e
    raise HTTPException(status_code=500, detail="Failed to create player")


@app_router.post("/team/join", response_model=TeamData, tags=["Team"])
async def join_team(request: TeamDataInput) -> TeamData:
    log.info(f"Joining team with data: {request}")
    try:
        team_joined = await GatewayService.join_team(request)
        if team_joined:
            log.info(f"Team joined: {team_joined}")
            return team_joined
    except TeamError as e:
        raise e
    raise HTTPException(status_code=500, detail="Failed to join team")


@app_router.post("/player/join", response_model=TeamDetails, tags=["Team"])
async def join_player(request: PlayerDataInput) -> TeamDetails:
    log.info(f"Player joining team with data: {request}")
    try:
        team_data = await GatewayService.get_players_data(request)
        if team_data:
            log.info(f"Team joined: {team_data}")
            return team_data
    except TeamError as e:
        raise e
    raise HTTPException(status_code=500, detail="Failed to join team")
