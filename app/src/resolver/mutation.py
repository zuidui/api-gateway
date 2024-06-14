import strawberry
from typing import Annotated, Optional

from resolver.team_schema import (
    TeamCreateType,
    TeamCreatedType,
    TeamCreateInput,
    TeamCreatedInput,
)

from resolver.player_schema import (
    PlayerCreateType,
    PlayerCreateInput,
    PlayerInfoType,
)

from resolver.rating_schema import (
    RatingType,
    RatingInput,
)

from data.cache import redis_client

from service.gateway_service import GatewayService


@strawberry.type
class Mutation:
    @strawberry.mutation(name="create_team")
    async def create_team(
        self,
        new_team: Annotated[TeamCreateInput, strawberry.argument(name="new_team")],
    ) -> Optional[TeamCreateType]:
        return await GatewayService.create_team_via_graphql(new_team)

    @strawberry.mutation(name="team_created")
    async def team_created(
        self,
        new_team: Annotated[TeamCreatedInput, strawberry.argument(name="new_team")],
    ) -> Optional[TeamCreatedType]:
        return await GatewayService.send_team_info_via_rest(new_team)

    @strawberry.mutation(name="create_player")
    async def create_player(
        self,
        new_player: Annotated[
            PlayerCreateInput, strawberry.argument(name="new_player")
        ],
    ) -> Optional[PlayerCreateType]:
        return await GatewayService.create_player_via_graphql(new_player)

    @strawberry.mutation(name="player_created")
    async def player_created(
        self,
        new_player: Annotated[
            PlayerCreateInput, strawberry.argument(name="new_player")
        ],
    ) -> Optional[PlayerInfoType]:
        team_id = new_player.player_team_id
        redis_client.set_message(f"team_message_{team_id}", new_player.player_name)
        return await GatewayService.player_info_check_and_consolidate(team_id)

    @strawberry.mutation(name="create_score")
    async def create_score(
        self,
        new_score: Annotated[RatingInput, strawberry.argument(name="new_score")],
    ) -> Optional[RatingType]:
        return await GatewayService.create_score_via_graphql(new_score)
