from typing import List
import strawberry

from resolver.player_schema import PlayerDataType, PlayerDetailsType


@strawberry.type
class TeamDataType:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")


@strawberry.input
class TeamDataInput:
    team_name: str = strawberry.field(name="team_name")
    team_password: str = strawberry.field(name="team_password")


@strawberry.input
class TeamModifiedInput:
    team_id: str = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")


@strawberry.type
class TeamInfoType:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")
    team_players: List[PlayerDataType] = strawberry.field(name="team_players")


@strawberry.input
class TeamInfoInput:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")
    players_data: List[PlayerDetailsType] = strawberry.field(name="players_data")
