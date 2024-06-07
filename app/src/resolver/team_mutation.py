import strawberry
from typing import Optional

from resolver.team_schema import TeamInput, TeamType

from service.team_service import TeamService


@strawberry.type
class TeamMutation:
    @strawberry.mutation(name="createTeam", description="Create a new team")
    async def create_team(self, new_team: TeamInput) -> Optional[TeamType]:
        return await TeamService.create_team_via_graphql(new_team)
