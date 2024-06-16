import httpx
from typing import Any, Dict, Optional

from exceptions.gateway_exceptions import (
    PlayerCreationError,
    TeamCreationError,
    TeamInfoError,
    TeamJoinError,
)

from utils.logger import logger_config
from utils.config import get_settings

from resolver.team_schema import (
    TeamDataInput,
    TeamDataType,
    TeamInfoInput,
    TeamInfoType,
    TeamModifiedInput,
)

from resolver.player_schema import (
    PlayerDataInput,
    PlayerDataType,
)


log = logger_config(__name__)
settings = get_settings()


class GatewayService:
    @staticmethod
    async def send_request(
        url: str, payload: Dict[str, Any]
    ) -> Optional[Dict[Any, Any]]:
        try:
            log.info(f"Sending request to {url} with payload: {payload}")
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                log.info(f"Response received: {response.json()}")
                return response.json()
        except httpx.HTTPStatusError as e:
            log.error(
                f"Request to {url} failed with status {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            log.error(f"An error occurred while requesting {e.request.url!r} - {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
        return {}

    @staticmethod
    async def create_team_via_graphql(
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
            raise TeamCreationError("No response received from the team service")

        created_team_data = response["data"]["create_team"]
        if created_team_data:
            created_team: Optional[TeamDataType] = TeamDataType(**created_team_data)
            log.info(f"Created team: {created_team}")
            return created_team

        error_messages = response["errors"][0]["message"]
        log.error(f"Error creating team: {error_messages}")
        raise TeamCreationError(error_messages)

    @staticmethod
    async def create_player_via_graphql(
        new_player: PlayerDataInput,
    ) -> Optional[PlayerDataType]:
        mutation = f"""
        mutation {{
            create_player (new_player: {{
                player_name: "{new_player.player_name}", 
                team_id: {new_player.team_id}
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
            raise PlayerCreationError("No response received from the team service")

        created_player_data = response["data"]["create_player"]
        if created_player_data:
            created_player: Optional[PlayerDataType] = PlayerDataType(
                **created_player_data
            )
            log.info(f"Created player: {created_player}")
            return created_player

        error_messages = response["errors"][0]["message"]
        log.error(f"Error creating player: {error_messages}")
        raise PlayerCreationError(error_messages)

    @staticmethod
    async def join_team_via_graphql(
        team_data: TeamDataInput,
    ) -> Optional[TeamDataType]:
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
            raise TeamJoinError("No response received from the team service")

        joined_team_data = response["data"]["join_team"]
        if joined_team_data:
            joined_team: Optional[TeamDataType] = TeamDataType(**joined_team_data)
            log.info(f"Joined team: {joined_team}")
            return joined_team

        error_messages = response["errors"][0]["message"]
        log.error(f"Error joining team: {error_messages}")
        raise TeamJoinError(error_messages)

    @staticmethod
    async def get_players_data_via_graphql(team_id: int) -> Optional[TeamInfoType]:
        query = f"""
        query {{
            get_players (team_id: {team_id}) {{
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
            raise TeamInfoError("No response received from the team service")

        players_data = response["data"]["get_players"]
        if players_data:
            team_info: Optional[TeamInfoType] = TeamInfoType(**players_data)
            log.info(f"Team info: {team_info}")
            return team_info

        error_messages = response["errors"][0]["message"]
        log.error(f"Error getting team info: {error_messages}")
        raise TeamInfoError(error_messages)

    @staticmethod
    async def send_team_info_via_rest(
        team_created: TeamModifiedInput,
    ) -> Optional[TeamDataType]:
        payload = {
            "teamId": team_created.team_id,
            "teamName": team_created.team_name,
        }
        response = await GatewayService.send_request(
            settings.FRONTEND_SERVICE_URL, payload
        )
        return TeamDataType(**response) if response else None

    @staticmethod
    async def send_team_details_via_rest(
        team_details: TeamInfoInput,
    ) -> Optional[TeamInfoType]:
        payload = {
            "teamId": team_details.team_id,
            "teamName": team_details.team_name,
            "playersData": team_details.players_data,
        }
        response = await GatewayService.send_request(
            settings.FRONTEND_SERVICE_URL, payload
        )
        return TeamInfoType(**response) if response else None
