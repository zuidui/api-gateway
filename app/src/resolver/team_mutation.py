import strawberry
from typing import Annotated, Optional

from resolver.team_schema import TeamCreateRequest, TeamCreateResponse

from service.team_service import TeamService


@strawberry.type
class TeamMutation:
    @strawberry.mutation(name="create_team")
    async def create_team(
        self,
        new_team: Annotated[TeamCreateRequest, strawberry.argument(name="new_team")],
    ) -> Optional[TeamCreateResponse]:
        return await TeamService.create_team_via_graphql(new_team)
