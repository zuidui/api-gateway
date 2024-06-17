import asyncio
from fastapi import FastAPI
import httpx
from typing import Any, Dict, Optional

from exceptions.gateway_exceptions import (
    TeamError,
    PlayerError,
)

from utils.logger import logger_config
from utils.config import get_settings

from resolver.team_schema import (
    TeamDataType,
)

from resolver.player_schema import (
    PlayerDataType,
)

from models.team_model import (
    TeamData,
    TeamDetails,
    TeamDataInput,
)

from models.player_model import (
    PlayerDataInput,
    PlayerDetails,
)


log = logger_config(__name__)
settings = get_settings()


class GatewayService:
    message_store: Dict[str, Any] = {}
    message_condition: Dict[str, asyncio.Condition] = {}

    @staticmethod
    async def send_request(
        url: str, payload: Dict[str, Any]
    ) -> Optional[Dict[Any, Any]]:
        try:
            log.info(f"Sending request to {url} with payload: {payload}")
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                log.info(f"Response received from {url}: {response.json()}")
                return response.json()
        except httpx.HTTPStatusError as e:
            log.error(
                f"Request to {url} failed with status {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            log.error(f"Request to {url} failed: {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
        return {}

    @staticmethod
    async def wait_for_event(event_type: str, timeout: int = 5) -> Optional[Any]:
        if event_type not in GatewayService.message_condition:
            GatewayService.message_condition[event_type] = asyncio.Condition()

        condition = GatewayService.message_condition[event_type]
        async with condition:
            try:
                await asyncio.wait_for(condition.wait(), timeout)
                return GatewayService.message_store.pop(event_type, None)
            except asyncio.TimeoutError:
                log.error(f"Timeout waiting for response to event type {event_type}")
                return None
            finally:
                if event_type in GatewayService.message_condition:
                    del GatewayService.message_condition[event_type]

    @staticmethod
    async def handle_message(
        app: FastAPI, message: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        event_type = message["event_type"]
        data = message["data"]
        result_dict: Optional[Dict[str, Any]] = None
        if event_type == "team_created" or event_type == "team_joined":
            result = TeamData(**data)
            result_dict = result.__dict__
        else:
            log.info(f"Event type {event_type} consumed but not handled.")
            result_dict = data

        if event_type in GatewayService.message_condition:
            async with GatewayService.message_condition[event_type]:
                GatewayService.message_store[event_type] = result_dict
                GatewayService.message_condition[event_type].notify_all()
        else:
            log.error(f"Event type {event_type} not being waited for.")
        return result_dict

    @staticmethod
    async def create_team(
        new_team: TeamDataInput,
    ) -> Optional[TeamDataType]:
        mutation = f"""
        mutation {{
            create_team (new_team: {{
                team_name: "{new_team.team_name}", 
                team_password: "{new_team.team_password}"
            }}) {{
                team_id
                team_name
            }}
        }}
        """
        response = await GatewayService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )

        if not response:
            raise TeamError("No response received from the team service")

        created_team_data = response["data"]["create_team"]
        if created_team_data:
            created_team: Optional[TeamDataType] = TeamDataType(**created_team_data)
            log.info(f"Created team: {created_team}")
            return created_team

        error_messages = response["errors"][0]["message"]
        log.error(f"Error creating team: {error_messages}")
        raise TeamError(error_messages)

    @staticmethod
    async def create_player(
        new_player: PlayerDataInput,
    ) -> Optional[PlayerDataType]:
        mutation = f"""
        mutation {{
            create_player (new_player: {{
                player_name: "{new_player.player_name}", 
                team_name: "{new_player.team_name}"
            }}) {{
                player_id
                player_name
            }}
        }}
        """
        response = await GatewayService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )

        if not response:
            raise PlayerError("No response received from the team service")

        created_player_data = response["data"]["create_player"]
        if created_player_data:
            created_player: Optional[PlayerDataType] = PlayerDataType(
                **created_player_data
            )
            log.info(f"Created player: {created_player}")
            return created_player

        error_messages = response["errors"][0]["message"]
        log.error(f"Error creating player: {error_messages}")
        raise PlayerError(error_messages)

    @staticmethod
    async def join_team(
        team_data: TeamDataInput,
    ) -> Optional[TeamData]:
        mutation = f"""
        mutation {{
            join_team (team_data: {{
                team_name: "{team_data.team_name}", 
                team_password: "{team_data.team_password}"
            }}) {{
                team_id
                team_name
            }}
        }}
        """
        response = await GatewayService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )

        if not response:
            raise TeamError("No response received from the team service")

        joined_team_data = response["data"]["join_team"]
        if joined_team_data:
            joined_team: Optional[TeamData] = TeamData(**joined_team_data)
            log.info(f"Joined team: {joined_team}")
            return joined_team

        error_messages = response["errors"][0]["message"]
        log.error(f"Error joining team: {error_messages}")
        raise TeamError(error_messages)

    @staticmethod
    async def get_players_name(team_name: str) -> Optional[Dict[str, Any]]:
        query = f"""
        query {{
            get_players (team_name: "{team_name}") {{
                team_id
                team_name
                players_data {{
                    player_id
                    player_name
                }}
            }}
        }}
        """
        response = await GatewayService.send_request(
            settings.TEAM_SERVICE_URL, {"query": query}
        )

        if not response:
            raise TeamError("No response received from the team service")

        players_data = response["data"]["get_players"]
        if players_data:
            log.info(f"Players data: {players_data}")
            return players_data

        error_messages = response["errors"][0]["message"]
        log.error(f"Error getting team info: {error_messages}")
        raise TeamError(error_messages)

    @staticmethod
    async def get_players_rating(team_id: int) -> Optional[Dict[str, Any]]:
        query = f"""
        query {{
            get_players_rating (team_id: {team_id}) {{
                team_id
                players_data {{
                    player_id
                    player_average_rating
                }}
            }}
        }}
        """
        response = await GatewayService.send_request(
            settings.RATING_SERVICE_URL, {"query": query}
        )

        if not response:
            raise TeamError("No response received from the rating service")

        players_data = response["data"]["get_players_rating"]
        if players_data:
            log.info(f"Players data: {players_data}")
            return players_data

        error_messages = response["errors"][0]["message"]
        log.error(f"Error getting team info: {error_messages}")
        raise TeamError(error_messages)

    @staticmethod
    async def get_players_data(player_data: PlayerDataInput) -> TeamDetails:
        players_data = await GatewayService.get_players_name(player_data.team_name)

        if not players_data:
            raise TeamError("No response received from the team service")

        players_rating = await GatewayService.get_players_rating(
            players_data["team_id"]
        )

        if not players_rating:
            raise TeamError("No response received from the rating service")

        player_ratings_dict = {
            rating["player_id"]: rating["player_average_rating"]
            for rating in players_rating["players_data"]
        }
        players_details = TeamDetails(
            team_id=players_data["team_id"],
            team_name=players_data["team_name"],
            players_data=[
                PlayerDetails(
                    player_name=player["player_name"],
                    player_average_rating=player_ratings_dict.get(
                        player["player_id"], None
                    ),
                )
                for player in players_data["players_data"]
            ],
        )
        return players_details
