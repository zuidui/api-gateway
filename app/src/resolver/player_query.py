import strawberry
from typing import Optional

from resolver.player_schema import PlayerType

from service.team_service import get_player_by_name_via_graphql as get_player_by_name


@strawberry.type
class PlayerQuery:
    player: Optional[PlayerType] = strawberry.field(resolver=get_player_by_name)
