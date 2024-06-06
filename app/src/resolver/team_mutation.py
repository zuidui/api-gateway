import strawberry
from typing import Optional

from resolver.team_schema import TeamInput, TeamType

from service.team_service import create_team_via_graphql


@strawberry.type
class TeamMutation:
    @strawberry.mutation
    async def create_team(self, new_team: TeamInput) -> Optional[TeamType]:
        return await create_team_via_graphql(new_team)
