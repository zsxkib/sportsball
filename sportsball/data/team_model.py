"""The prototype class for a team."""

from typing import Any, Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType
from .news_model import NewsModel
from .odds_model import OddsModel
from .player_model import PlayerModel

TEAM_POINTS_COLUMN: Literal["points"] = "points"
TEAM_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
PLAYER_COLUMN_PREFIX: Literal["players"] = "players"


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


class TeamModel(BaseModel):
    """The serialisable team class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=TEAM_IDENTIFIER_COLUMN,
    )
    name: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.TEXT})
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
    )
    news: list[NewsModel]
