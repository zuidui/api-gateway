import strawberry
from typing import Optional

from resolver.player_schema import PlayerInput, PlayerType

from service.team_service import create_player_via_graphql


@strawberry.type
class PlayerMutation:
    @strawberry.mutation
    async def create_player(self, new_player: PlayerInput) -> Optional[PlayerType]:
        return await create_player_via_graphql(new_player)
