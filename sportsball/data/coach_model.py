"""The prototype class for coach."""

from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType

COACH_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
COACH_NAME_COLUMN: Literal["name"] = "name"


class CoachModel(BaseModel):
    """The serialisable coach class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=COACH_IDENTIFIER_COLUMN,
    )
    name: str = Field(..., alias=COACH_NAME_COLUMN)
