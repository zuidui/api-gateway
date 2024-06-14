import strawberry


@strawberry.type
class RatingType:
    player_id: int = strawberry.field(name="player_id")
    player_score: int = strawberry.field(name="player_score")
    player_team_id: int = strawberry.field(name="player_team_id")


@strawberry.input
class RatingInput:
    player_id: int = strawberry.field(name="player_id")
    player_score: int = strawberry.field(name="player_score")
    player_team_id: int = strawberry.field(name="player_team_id")
