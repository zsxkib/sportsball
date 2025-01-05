"""The prototype class for a player."""

from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType

PLAYER_KICKS_COLUMN: Literal["kicks"] = "kicks"
PLAYER_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
PLAYER_FUMBLES_COLUMN: Literal["fumbles"] = "fumbles"


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
