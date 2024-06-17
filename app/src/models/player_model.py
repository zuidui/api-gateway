from pydantic import BaseModel


class PlayerDetails(BaseModel):
    player_name: str
    player_average_rating: float


class PlayerDataInput(BaseModel):
    team_name: str
    player_name: str
