from typing import List
import strawberry


@strawberry.input
class PlayerRatingInputType:
    player_id: int = strawberry.field(name="player_id")
    player_average_rating: float = strawberry.field(name="player_average_rating")


@strawberry.input
class PlayerRatingInput:
    team_id: int = strawberry.field(name="team_id")
    players: List[PlayerRatingInputType] = strawberry.field(name="players")
