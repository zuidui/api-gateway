import httpx
from typing import Any, Dict, Optional

from utils.logger import logger_config
from utils.config import get_settings

from resolver.team_schema import TeamType, TeamInput
from resolver.player_schema import PlayerType, PlayerInput

log = logger_config(__name__)
settings = get_settings()


class TeamService:
    @staticmethod
    async def send_request(
        url: str, payload: Dict[str, Any]
    ) -> Optional[Dict[Any, Any]]:
        try:
            log.debug(f"Sending request to {url} with payload: {payload}")
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                log.debug(f"Response received: {response.json()}")
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
    async def create_team_via_graphql(new_team: TeamInput) -> Optional[TeamType]:
        mutation = f"""
        mutation {{
            createTeam (newTeam: {{teamName: "{new_team.teamName}", teamPassword: "{new_team.teamPassword}"}}) {{
                teamId
                teamName
            }}
        }}
        """
        log.debug(f"Mutation: {mutation}")
        data = await TeamService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )
        if data and "createTeam" in data:
            log.debug(f"Data: {data}")
            created_team: Optional[TeamType] = TeamType(**data["createTeam"])
        else:
            log.error(f"Error creating team: {data}")
            created_team = None
        return created_team

    @staticmethod
    async def create_player_via_graphql(
        new_player: PlayerInput,
    ) -> Optional[PlayerType]:
        mutation = f"""
        mutation {{
            createPlayer (playerName: "{new_player.playerName}", teamId: "{new_player.teamId}") {{
                teamId
                playerName
            }}
        }}
        """
        log.debug(f"Mutation: {mutation}")
        data = await TeamService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )
        created_player: Optional[PlayerType] = (
            PlayerType(**data["createPlayer"]) if data else None
        )
        log.debug(f"Player created: {created_player}")
        return created_player

    @staticmethod
    async def get_team_by_name_via_graphql(team: TeamInput) -> Optional[TeamType]:
        query = f"""
        query {{
            getTeamByName: (teamName: "{team.teamName}") {{
                teamName
            }}
        }}
        """
        log.debug(f"Query: {query}")
        data = await TeamService.send_request(
            settings.TEAM_SERVICE_URL, {"query": query}
        )
        retrieved_team: Optional[TeamType] = (
            TeamType(**data["getTeamByName"]) if data else None
        )
        log.debug(f"Team found: {retrieved_team}")
        return retrieved_team

    @staticmethod
    async def get_player_by_name_via_graphql(
        player: PlayerInput,
    ) -> Optional[PlayerType]:
        query = f"""
        query {{
            getPlayerByName (playerName: "{player.playerName}", teamId: "{player.teamId}") {{
                playerName
                teamId
            }}
        }}
        """
        log.debug(f"Query: {query}")
        data = await TeamService.send_request(
            settings.TEAM_SERVICE_URL, {"query": query}
        )
        retrieved_player: Optional[PlayerType] = (
            PlayerType(**data["getPlayerByName"]) if data else None
        )
        log.debug(f"Player found: {retrieved_player}")
        return retrieved_player

    @staticmethod
    async def team_created_via_rest(
        team_created: TeamType,
    ) -> Optional[TeamType]:
        log.debug(f"The team created is: {team_created}")
        payload = {
            "teamId": team_created.teamId,
            "teamName": team_created.teamName,
        }
        await TeamService.send_request(settings.FRONTEND_SERVICE_URL, payload)
        return team_created
