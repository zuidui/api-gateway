import json
import httpx
from typing import Any, Dict, Optional

from exceptions.gateway_exceptions import (
    PlayerCreationError,
    RatingCreationError,
    TeamCreationError,
    TeamJoinError,
)

from utils.logger import logger_config
from utils.config import get_settings
from data.cache import redis_client

from resolver.team_schema import (
    TeamCreateType,
    TeamCreatedType,
    TeamCreateInput,
    TeamCreatedInput,
    TeamDataInput,
    TeamDataType,
)

from resolver.player_schema import (
    PlayerCreateType,
    PlayerCreateInput,
    PlayerInfoType,
    PlayerInfoInput,
)

from resolver.rating_schema import (
    RatingInput,
    RatingType,
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
        response = await GatewayService.send_request(
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
        response = await GatewayService.send_request(
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
    async def create_score_via_graphql(
        new_score: RatingInput,
    ) -> Optional[RatingType]:
        mutation = f"""
        mutation {{
            create_score (new_score: {{
                player_id: {new_score.player_id},
                player_score: "{new_score.player_score}", 
                player_team_id: {new_score.player_team_id}
            }}) {{
                player_id
                player_score
                player_team_id
            }}
        }}
        """
        response = await GatewayService.send_request(
            settings.RATING_SERVICE_URL, {"query": mutation}
        )

        if not response:
            raise RatingCreationError("No response received from the rating service")

        created_score_data = response["data"]["create_score"]
        if created_score_data:
            created_score: Optional[RatingType] = RatingType(**created_score_data)
            log.info(f"Created score: {created_score}")
            return created_score

        error_messages = response["errors"][0]["message"]
        log.error(f"Error creating player: {error_messages}")
        raise RatingCreationError(error_messages)

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
    async def send_team_info_via_rest(
        team_created: TeamCreatedInput,
    ) -> Optional[TeamCreatedType]:
        payload = {
            "teamId": team_created.team_id,
            "teamName": team_created.team_name,
        }
        response = await GatewayService.send_request(
            settings.FRONTEND_SERVICE_URL, payload
        )
        return TeamCreatedType(**response) if response else None

    @staticmethod
    async def send_player_info_via_rest(
        player_info: PlayerInfoInput,
    ) -> Optional[PlayerInfoType]:
        payload = {
            "playerName": player_info.player_name,
            "playerScore": player_info.player_score,
        }
        response = await GatewayService.send_request(
            settings.FRONTEND_SERVICE_URL, payload
        )
        return PlayerInfoType(**response) if response else None

    @staticmethod
    async def player_info_check_and_consolidate(
        player_id: int,
    ) -> Optional[PlayerInfoType]:
        team_message = redis_client.get_message(f"team_message_{player_id}")
        rating_message = redis_client.get_message(f"rating_message_{player_id}")
        if team_message and rating_message:
            player_data = json.loads(team_message)
            rating_data = json.loads(rating_message)
            team_name = player_data["player_team_name"]
            player_name = player_data["player_name"]
            player_info = PlayerInfoInput(
                player_id=player_id,
                player_team_id=player_data["player_team_id"],
                player_name=player_name,
                player_score=rating_data["player_score"],
            )
            await GatewayService.send_player_info_via_rest(player_info)
            redis_client.set_message(f"team_message_{player_id}", "")
            redis_client.set_message(f"rating_message_{player_id}", "")
            return PlayerInfoType(
                player_team_id=player_info.player_team_id,
                player_name=player_name,
                player_team_name=team_name,
                player_score=player_info.player_score,
            )
        return None
