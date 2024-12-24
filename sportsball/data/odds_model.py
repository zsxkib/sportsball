"""The prototype class for odds."""

from pydantic import BaseModel, Field

from .bookie_model import BookieModel
from .field_type import TYPE_KEY, FieldType


class OddsModel(BaseModel):
    """The serialisable odds class."""

    odds: float = Field(..., json_schema_extra={TYPE_KEY: FieldType.ODDS})
    bookie: BookieModel
