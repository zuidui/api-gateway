import strawberry
from typing import Optional

from resolver.player_schema import PlayerType

from service.team_service import TeamService


@strawberry.type
class PlayerQuery:
    player: Optional[PlayerType] = strawberry.field(
        resolver=TeamService.get_player_by_name_via_graphql
    )
