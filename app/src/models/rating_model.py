from pydantic import BaseModel
from typing import List


class PlayerScore(BaseModel):
    player_name: str
    player_score: int


class TeamScoreInput(BaseModel):
    team_name: str
    players_data: List[PlayerScore]


class PlayerRating(BaseModel):
    player_id: int
    player_score: int


class TeamRatingInput(BaseModel):
    team_id: int
    players_data: List[PlayerRating]
