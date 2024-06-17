import strawberry


@strawberry.type
class PlayerDataType:
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")


@strawberry.input
class PlayerDataInput:
    team_name: str = strawberry.field(name="team_name")
    player_name: str = strawberry.field(name="player_name")


@strawberry.type
class PlayerDetailsType:
    player_name: str = strawberry.field(name="player_name")
    player_average_rating: float = strawberry.field(name="player_average_rating")


@strawberry.input
class PlayerDetailsInput:
    team_id: int = strawberry.field(name="team_id")
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")
    player_average_rating: float = strawberry.field(name="player_average_rating")
