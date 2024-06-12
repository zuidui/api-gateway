import strawberry
from typing import Annotated, Optional

from resolver.team_schema import (
    TeamCreateType,
    TeamCreatedType,
    TeamCreateInput,
    TeamCreatedInput,
)

from service.team_service import TeamService


@strawberry.type
class TeamMutation:
    @strawberry.mutation(name="create_team")
    async def create_team(
        self,
        new_team: Annotated[TeamCreateInput, strawberry.argument(name="new_team")],
    ) -> Optional[TeamCreateType]:
        return await TeamService.create_team_via_graphql(new_team)

    @strawberry.mutation(name="team_created")
    async def team_created(
        self,
        new_team: Annotated[TeamCreatedInput, strawberry.argument(name="new_team")],
    ) -> Optional[TeamCreatedType]:
        return await TeamService.team_created_via_rest(new_team)
