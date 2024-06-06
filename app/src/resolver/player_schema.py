import strawberry


@strawberry.type
class PlayerType:
    playerId: int
    teamId: int
    playerName: str
    created_at: str


@strawberry.input
class PlayerInput:
    teamId: int
    playerName: str
