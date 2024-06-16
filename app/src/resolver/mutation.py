import strawberry
from typing import Annotated, Optional

from resolver.team_schema import (
    TeamDataType,
    TeamInfoInput,
    TeamInfoType,
    TeamModifiedInput,
)

from resolver.player_schema import PlayerDetailsType

from resolver.rating_schema import PlayerRatingInput


from service.gateway_service import GatewayService


@strawberry.type
class Mutation:
    @strawberry.mutation(name="team_created")
    async def team_created(
        self,
        new_team: Annotated[TeamModifiedInput, strawberry.argument(name="new_team")],
    ) -> Optional[TeamDataType]:
        return await GatewayService.send_team_info_via_rest(new_team)    

    @strawberry.mutation(name="team_joined")
    async def team_joined(
        self,
        team_data: Annotated[TeamModifiedInput, strawberry.argument(name="team_data")],
    ) -> Optional[TeamDataType]:
        return await GatewayService.send_team_info_via_rest(team_data)

    @strawberry.mutation(name="rating_updated")
    async def rating_updated(
        self,
        team_data: Annotated[PlayerRatingInput, strawberry.argument(name="team_data")],
    ) -> Optional[TeamInfoType]:
        players_data = await GatewayService.get_players_data_via_graphql(
            team_data.team_id
        )

        if not players_data:
            return None

        team_data_dict = {
            player.player_id: player.player_average_rating
            for player in team_data.players
        }

        players_details = [
            PlayerDetailsType(
                player_name=player.player_name,
                player_average_rating=team_data_dict[player.player_id],
            )
            for player in players_data.team_players
            if player.player_id in team_data_dict
        ]

        team_details = TeamInfoInput(
            team_id=players_data.team_id,
            team_name=players_data.team_name,
            players_data=players_details,
        )
        return await GatewayService.send_team_details_via_rest(team_details)
