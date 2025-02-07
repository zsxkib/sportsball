"""A class for holding address information."""

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType
from .weather_model import WeatherModel


class AddressModel(BaseModel):
    """The class for representing an address."""

    city: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    state: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    zipcode: str | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL}
    )
    latitude: float | None
    longitude: float | None
    housenumber: str | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL}
    )
    weather: WeatherModel | None
    timezone: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    country: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
