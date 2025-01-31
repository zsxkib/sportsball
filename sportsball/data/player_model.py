"""The prototype class for a player."""

from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType

PLAYER_KICKS_COLUMN: Literal["kicks"] = "kicks"
PLAYER_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
PLAYER_FUMBLES_COLUMN: Literal["fumbles"] = "fumbles"
PLAYER_FUMBLES_LOST_COLUMN: Literal["fumbles_lost"] = "fumbles_lost"
FIELD_GOALS_COLUMN: Literal["field_goals"] = "field_goals"
FIELD_GOALS_ATTEMPTED_COLUMN: Literal["field_goals_attempted"] = "field_goals_attempted"
OFFENSIVE_REBOUNDS_COLUMN: Literal["offensive_rebounds"] = "offensive_rebounds"
ASSISTS_COLUMN: Literal["assists"] = "assists"
TURNOVERS_COLUMN: Literal["turnovers"] = "turnovers"


class PlayerModel(BaseModel):
    """The serialisable player class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=PLAYER_IDENTIFIER_COLUMN,
    )
    jersey: str | None = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKS_COLUMN,
    )
    fumbles: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_COLUMN,
    )
    fumbles_lost: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_LOST_COLUMN,
    )
    field_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_COLUMN,
    )
    field_goals_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_ATTEMPTED_COLUMN,
    )
    offensive_rebounds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=OFFENSIVE_REBOUNDS_COLUMN,
    )
    assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=ASSISTS_COLUMN,
    )
    turnovers: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=TURNOVERS_COLUMN,
    )
