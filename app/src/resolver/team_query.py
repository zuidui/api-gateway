import strawberry
from typing import Optional

from resolver.team_schema import TeamType

from service.team_service import get_team_by_name_via_graphql as get_team_by_name


@strawberry.type
class TeamQuery:
    Team: Optional[TeamType] = strawberry.field(resolver=get_team_by_name)
