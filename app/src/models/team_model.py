from pydantic import BaseModel
from typing import List

from models.player_model import PlayerDataName, PlayerDetails


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


class TeamInfo(BaseModel):
    team_id: int
    team_name: str
    players_data: List[TeamData]


class TeamInfoData(BaseModel):
    team_id: int
    team_name: str
    players_data: List[PlayerDataName]


class TeamDetails(BaseModel):
    team_id: int
    team_name: str
    players_data: List[PlayerDetails]
