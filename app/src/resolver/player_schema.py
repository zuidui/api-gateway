import strawberry


@strawberry.type
class PlayerCreateType:
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")


@strawberry.type
class PlayerInfoType:
    player_team_id: int = strawberry.field(name="player_team_id")
    player_name: str = strawberry.field(name="player_name")
    player_team_name: str = strawberry.field(name="player_team_name")
    player_score: int = strawberry.field(name="player_score")


@strawberry.input
class PlayerCreateInput:
    player_team_id: int = strawberry.field(name="player_team_id")
    player_name: str = strawberry.field(name="player_name")


@strawberry.input
class PlayerInfoInput:
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")
    player_team_id: int = strawberry.field(name="player_team_id")
    player_score: int = strawberry.field(name="player_score")
