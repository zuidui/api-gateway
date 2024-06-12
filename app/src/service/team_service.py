import httpx
from typing import Any, Dict, Optional

from exceptions.team_exceptions import PlayerCreationError, TeamCreationError

from utils.logger import logger_config
from utils.config import get_settings

from resolver.team_schema import (
    TeamCreateType,
    TeamCreatedType,
    TeamCreateInput,
    TeamCreatedInput,
)

from resolver.player_schema import (
    PlayerCreateType,
    PlayerCreatedType,
    PlayerCreatedInput,
    PlayerCreateInput,
)

log = logger_config(__name__)
settings = get_settings()


class TeamService:
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
            log.error(f"An error occurred while requesting {e.request.url!r}.")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
        return {}

    @staticmethod
    async def create_team_via_graphql(
        new_team: TeamCreateInput,
    ) -> Optional[TeamCreateType]:
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
        response = await TeamService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )

        if not response:
            raise TeamCreationError("No response received from the team service")

        created_team_data = response["data"]["create_team"]
        if created_team_data:
            created_team: Optional[TeamCreateType] = TeamCreateType(**created_team_data)
            log.info(f"Created team: {created_team}")
            return created_team

        error_messages = response["errors"][0]["message"]
        log.error(f"Error creating team: {error_messages}")
        raise TeamCreationError(error_messages)

    @staticmethod
    async def team_created_via_rest(
        team_created: TeamCreatedInput,
    ) -> Optional[TeamCreatedType]:
        payload = {
            "teamId": team_created.team_id,
            "teamName": team_created.team_name,
        }
        response = await TeamService.send_request(
            settings.FRONTEND_SERVICE_URL, payload
        )
        return TeamCreatedType(**response) if response else None

    @staticmethod
    async def create_player_via_graphql(
        new_player: PlayerCreateInput,
    ) -> Optional[PlayerCreateType]:
        mutation = f"""
        mutation {{
            create_player (new_player: {{
                player_name: "{new_player.player_name}", 
                player_team_id: {new_player.player_team_id}
            }}) {{
                player_id
                player_name
            }}
        }}
        """
        response = await TeamService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )

        if not response:
            raise PlayerCreationError("No response received from the team service")

        created_player_data = response["data"]["create_player"]
        if created_player_data:
            created_player: Optional[PlayerCreateType] = PlayerCreateType(
                **created_player_data
            )
            log.info(f"Created player: {created_player}")
            return created_player

        error_messages = response["errors"][0]["message"]
        log.error(f"Error creating player: {error_messages}")
        raise PlayerCreationError(error_messages)

    @staticmethod
    async def player_created_via_rest(
        player_created: PlayerCreatedInput,
    ) -> Optional[PlayerCreatedType]:
        payload = {
            "teamId": player_created.player_team_id,
            "playerTeamName": player_created.player_team_name,
            "playerName": player_created.player_name,
            "playerScore": player_created.player_score,
        }
        response = await TeamService.send_request(
            settings.FRONTEND_SERVICE_URL, payload
        )

        return PlayerCreatedType(**response) if response else None
