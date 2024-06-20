from pydantic import BaseModel


class PlayerDetails(BaseModel):
    player_name: str
    player_average_rating: float


class PlayerData(BaseModel):
    player_id: int
    player_average_rating: float


class PlayerDataName(BaseModel):
    player_id: int
    player_name: str


class PlayerDataInput(BaseModel):
    team_name: str
    player_name: str
