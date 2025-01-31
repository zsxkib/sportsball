"""The prototype class for odds."""

import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .bookie_model import BookieModel
from .field_type import TYPE_KEY, FieldType

DT_COLUMN: Literal["dt"] = "dt"


class OddsModel(BaseModel):
    """The serialisable odds class."""

    odds: float = Field(..., json_schema_extra={TYPE_KEY: FieldType.ODDS})
    bookie: BookieModel
    dt: datetime.datetime | None = Field(
        ...,
        alias=DT_COLUMN,
    )
