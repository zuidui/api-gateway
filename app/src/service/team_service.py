import httpx
from typing import Any, Dict, Optional

from utils.logger import logger_config
from utils.config import get_settings

from resolver.team_schema import TeamType, TeamInput
from resolver.player_schema import PlayerType, PlayerInput

log = logger_config(__name__)
settings = get_settings()


async def send_request(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        log.debug(
            f"Sending request to {settings.TEAM_SERVICE_URL} with payload: {payload}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.TEAM_SERVICE_URL}", json=payload)
            response.raise_for_status()
            log.debug(f"Response received: {response.json()}")
            return response.json().get("data")
    except httpx.HTTPStatusError as e:
        log.error(
            f"Request failed with status {e.response.status_code}: {e.response.text}"
        )
    except httpx.RequestError as e:
        log.error(f"An error occurred while requesting {e.request.url!r}.")
    except Exception as e:
        log.error(f"Unexpected error: {e}")
    return None


async def create_team_via_graphql(new_team: TeamInput) -> Optional[TeamType]:
    mutation = f"""
    mutation {{
        createTeam (newTeam: {{teamName: "{new_team.teamName}", teamPassword: "{new_team.teamPassword}"}}) {{
            teamName
            teamPassword
        }}
    }}
    """
    log.debug(f"Mutation: {mutation}")
    data = await send_request({"query": mutation})
    if data and "createTeam" in data:
        created_team: Optional[TeamType] = TeamType(**data["createTeam"])
    else:
        created_team = None
    log.debug(f"Team created: {created_team}")
    return created_team


async def create_player_via_graphql(new_player: PlayerInput) -> Optional[PlayerType]:
    mutation = f"""
    mutation {{
        createPlayer (playerName: "{new_player.playerName}", teamId: "{new_player.teamId}") {{
            teamId
            playerName
        }}
    }}
    """
    log.debug(f"Mutation: {mutation}")
    data = await send_request({"query": mutation})
    created_player: Optional[PlayerType] = (
        PlayerType(**data["createPlayer"]) if data else None
    )
    log.debug(f"Player created: {created_player}")
    return created_player


async def get_team_by_name_via_graphql(team: TeamInput) -> Optional[TeamType]:
    query = f"""
    query {{
        getTeamByName: (teamName: "{team.teamName}") {{
            teamName
        }}
    }}
    """
    log.debug(f"Query: {query}")
    data = await send_request({"query": query})
    retrieved_team: Optional[TeamType] = (
        TeamType(**data["getTeamByName"]) if data else None
    )
    log.debug(f"Team found: {retrieved_team}")
    return retrieved_team


async def get_player_by_name_via_graphql(player: PlayerInput) -> Optional[PlayerType]:
    query = f"""
    query {{
        getPlayerByName (playerName: "{player.playerName}", teamId: "{player.teamId}") {{
            playerName
            teamId
        }}
    }}
    """
    log.debug(f"Query: {query}")
    data = await send_request({"query": query})
    retrieved_player: Optional[PlayerType] = (
        PlayerType(**data["getPlayerByName"]) if data else None
    )
    log.debug(f"Player found: {retrieved_player}")
    return retrieved_player
