from pydantic import BaseModel
from typing import List

from models.player_model import PlayerDetails


class TeamData(BaseModel):
    team_id: int
    team_name: str


class TeamDataInput(BaseModel):
    team_name: str
    team_password: str


class TeamJoinInput(BaseModel):
    team_name: str
    team_password: str
    player_name: str


class TeamDetails(BaseModel):
    team_id: int
    team_name: str
    players_data: List[PlayerDetails]
