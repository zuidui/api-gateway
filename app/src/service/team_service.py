import httpx
from typing import Any, Dict, Optional

from utils.logger import logger_config
from utils.config import get_settings

from resolver.team_schema import TeamCreateRequest, TeamCreateResponse

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
    async def create_team_via_graphql(
        new_team: TeamCreateRequest,
    ):
        # ) -> Optional[TeamCreateResponse]:
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
        log.debug(f"Mutation: {mutation}")
        response = await TeamService.send_request(
            settings.TEAM_SERVICE_URL, {"query": mutation}
        )

        if response:
            created_team_data = response["data"]["create_team"]
            if created_team_data:
                log.debug(f"Created team: {created_team_data}")
                created_team: Optional[TeamCreateResponse] = TeamCreateResponse(**created_team_data)
            else:
                error_messages = response["errors"]
                if error_messages:
                    for error in error_messages:
                        log.error(f"{error['message']}")
                else:
                    log.error(f"Unexpected response format: {response}")
                created_team = None
        else:
            log.error("No response received from the team service")
            created_team = None
        return created_team

    @staticmethod
    async def team_created_via_rest(
        team_created: TeamCreateResponse,
    ) -> Optional[TeamCreateResponse]:
        log.debug(f"The team created is: {team_created}")
        payload = {
            "teamId": team_created.team_id,
            "teamName": team_created.team_name,
        }
        await TeamService.send_request(settings.FRONTEND_SERVICE_URL, payload)
        return team_created
