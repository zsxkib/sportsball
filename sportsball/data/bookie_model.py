"""The prototype class for a bookie."""

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType


class BookieModel(BaseModel):
    """The serialisable bookie class."""

    identifier: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    name: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.TEXT})
