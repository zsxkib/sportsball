"""The prototype class for a team."""

from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType
from .odds_model import OddsModel
from .player_model import PlayerModel

TEAM_POINTS_COLUMN: Literal["points"] = "points"
TEAM_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
PLAYER_COLUMN_PREFIX: Literal["players"] = "players"


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
