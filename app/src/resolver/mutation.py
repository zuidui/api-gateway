import json
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
    PlayerCreatedType,
    PlayerCreateInput,
    PlayerCreatedInput,
)

from resolver.message_schema import MessageInput, MessageResponse

from utils.cache import redis_client

from service.team_service import TeamService


@strawberry.type
class Mutation:
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
    
    @strawberry.mutation(name="create_player")
    async def create_player(
        self,
        new_player: Annotated[
            PlayerCreateInput, strawberry.argument(name="new_player")
        ],
    ) -> Optional[PlayerCreateType]:
        return await TeamService.create_player_via_graphql(new_player)

    @strawberry.mutation(name="player_created")
    async def player_created(
        self,
        input: Annotated[MessageInput, strawberry.argument(name="input")],
    ) -> MessageResponse:
        redis_client.set_message(f"team_message_{input.id}", input.message)
        await check_and_consolidate(input.id)
        return MessageResponse(status="team message received")

    @strawberry.mutation(name="score_created")
    async def score_created(
        self,
        input: Annotated[MessageInput, strawberry.argument(name="input")],
    ) -> MessageResponse:
        redis_client.set_message(f"score_message_{input.id}", input.message)
        await check_and_consolidate(input.id)
        return MessageResponse(status="score message received")


async def check_and_consolidate(player_id: str) -> Optional[PlayerCreatedType]:
    team_message = redis_client.get_message(f"team_message_{player_id}")
    score_message = redis_client.get_message(f"score_message_{player_id}")
    if team_message and score_message:
        player_data = json.loads(team_message)
        score_data = json.loads(score_message)
        player_created = PlayerCreatedInput(
            player_team_id=player_data["player_team_id"],
            player_name=player_data["player_name"],
            player_team_name=player_data["player_team_name"],
            player_score=score_data["player_score"],
        )
        await TeamService.player_created_via_rest(player_created)
        redis_client.set_message(f"player_message_{id}", "")
        redis_client.set_message(f"score_message_{id}", "")
        return PlayerCreatedType(
            player_team_id=player_data["player_team_id"],
            player_name=player_data["player_name"],
            player_team_name=player_data["player_team_name"],
            player_score=score_data["player_score"],
        )
    return None
