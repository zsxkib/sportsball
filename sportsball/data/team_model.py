"""The prototype class for a team."""

# pylint: disable=duplicate-code
from typing import Any, Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType
from .news_model import NewsModel
from .odds_model import OddsModel
from .player_model import PlayerModel
from .social_model import SocialModel

TEAM_POINTS_COLUMN: Literal["points"] = "points"
TEAM_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
PLAYER_COLUMN_PREFIX: Literal["players"] = "players"
NAME_COLUMN: Literal["name"] = "name"
FIELD_GOALS_COLUMN: Literal["field_goals"] = "field_goals"
FIELD_GOALS_ATTEMPTED_COLUMN: Literal["field_goals_attempted"] = "field_goals_attempted"
OFFENSIVE_REBOUNDS_COLUMN: Literal["offensive_rebounds"] = "offensive_rebounds"
ASSISTS_COLUMN: Literal["assists"] = "assists"
TURNOVERS_COLUMN: Literal["turnovers"] = "turnovers"
KICKS_COLUMN: Literal["kicks"] = "kicks"


def _calculate_kicks(data: dict[str, Any]) -> int | None:
    kicks = 0
    found_kicks = False
    for player in data[PLAYER_COLUMN_PREFIX]:
        player_kicks = player.kicks
        if player_kicks is None:
            continue
        found_kicks = True
        kicks += player_kicks
    if not found_kicks:
        return None
    return kicks


def _calculate_field_goals(data: dict[str, Any]) -> int | None:
    field_goals = 0
    found_field_goals = False
    for player in data[PLAYER_COLUMN_PREFIX]:
        player_field_goals = player.field_goals
        if player_field_goals is None:
            continue
        found_field_goals = True
        field_goals += player_field_goals
    if not found_field_goals:
        return None
    return field_goals


def _calculate_field_goals_attempted(data: dict[str, Any]) -> int | None:
    field_goals_attempted = 0
    found_field_goals_attempted = False
    for player in data[PLAYER_COLUMN_PREFIX]:
        player_field_goals_attempted = player.field_goals_attempted
        if player_field_goals_attempted is None:
            continue
        found_field_goals_attempted = True
        field_goals_attempted += player_field_goals_attempted
    if not found_field_goals_attempted:
        return None
    return field_goals_attempted


def _calculate_offensive_rebounds(data: dict[str, Any]) -> int | None:
    offensive_rebounds = 0
    found_offensive_rebounds = False
    for player in data[PLAYER_COLUMN_PREFIX]:
        player_offensive_rebounds = player.offensive_rebounds
        if player_offensive_rebounds is None:
            continue
        found_offensive_rebounds = True
        offensive_rebounds += player_offensive_rebounds
    if not found_offensive_rebounds:
        return None
    return offensive_rebounds


def _calculate_assists(data: dict[str, Any]) -> int | None:
    assists = 0
    found_assists = False
    for player in data[PLAYER_COLUMN_PREFIX]:
        player_assists = player.assists
        if player_assists is None:
            continue
        found_assists = True
        assists += player_assists
    if not found_assists:
        return None
    return assists


def _calculate_turnovers(data: dict[str, Any]) -> int | None:
    turnovers = 0
    found_turnovers = False
    for player in data[PLAYER_COLUMN_PREFIX]:
        player_turnovers = player.turnovers
        if player_turnovers is None:
            continue
        found_turnovers = True
        turnovers += player_turnovers
    if not found_turnovers:
        return None
    return turnovers


class TeamModel(BaseModel):
    """The serialisable team class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=TEAM_IDENTIFIER_COLUMN,
    )
    name: str = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.TEXT}, alias=NAME_COLUMN
    )
    location: str | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL}
    )
    players: list[PlayerModel] = Field(..., alias=PLAYER_COLUMN_PREFIX)
    odds: list[OddsModel]
    points: float | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.POINTS}, alias=TEAM_POINTS_COLUMN
    )
    ladder_rank: int | None
    kicks: int | None = Field(
        default_factory=_calculate_kicks,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=KICKS_COLUMN,
    )
    news: list[NewsModel]
    social: list[SocialModel]
    field_goals: int | None = Field(
        default_factory=_calculate_field_goals,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_COLUMN,
    )
    field_goals_attempted: int | None = Field(
        default_factory=_calculate_field_goals_attempted,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_ATTEMPTED_COLUMN,
    )
    offensive_rebounds: int | None = Field(
        default_factory=_calculate_offensive_rebounds,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=OFFENSIVE_REBOUNDS_COLUMN,
    )
    assists: int | None = Field(
        default_factory=_calculate_assists,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=ASSISTS_COLUMN,
    )
    turnovers: int | None = Field(
        default_factory=_calculate_turnovers,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=TURNOVERS_COLUMN,
    )
