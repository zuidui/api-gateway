from typing import Annotated, Optional
import strawberry

from resolver.player_schema import PlayerInfoType
from resolver.rating_schema import RatingInput

from service.gateway_service import GatewayService

from data.cache import redis_client


@strawberry.type
class Query:
    @strawberry.field(name="player_rating_info")
    async def get_player_info(
        self,
        player_data: Annotated[RatingInput, strawberry.argument(name="player_data")],
    ) -> Optional[PlayerInfoType]:
        redis_client.set_message(
            f"rating_message_{player_data.player_team_id}",
            str(player_data.player_score),
        )
        return await GatewayService.player_info_check_and_consolidate(
            player_data.player_team_id
        )
