"""A class for holding address information."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import pandas as pd
import requests

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      update_columns_list)
from .model import Model
from .weather_model import WeatherModel

ADDRESS_COLUMN_SUFFIX = "address"
CITY_COLUMN = "city"
STATE_COLUMN = "state"
ZIPCODE_COLUMN = "zipcode"
ADDRESS_LATITUDE_COLUMN = "latitude"
ADDRESS_LONGITUDE_COLUMN = "longitude"
ADDRESS_HOUSENUMBER_COLUMN = "housenumber"


class AddressModel(Model):
    """The class for representing an address."""

    def __init__(
        self, session: requests.Session, city: str, state: str, zipcode: str
    ) -> None:
        super().__init__(session)
        self._city = city
        self._state = state
        self._zipcode = zipcode

    @property
    def city(self) -> str:
        """Return the city."""
        return self._city

    @property
    def state(self) -> str:
        """Return the state."""
        return self._state

    @property
    def zipcode(self) -> str:
        """Return the zipcode."""
        return self._zipcode

    @property
    def latitude(self) -> float | None:
        """Return the latitude."""
        return None

    @property
    def longitude(self) -> float | None:
        """Return the longitude."""
        return None

    @property
    def housenumber(self) -> str | None:
        """Return the housenumber."""
        return None

    @property
    def weather(self) -> WeatherModel | None:
        """Return the weather."""
        return None

    def to_frame(self) -> pd.DataFrame:
        """Render the address as a dataframe."""
        data: dict[str, list[str | float]] = {
            CITY_COLUMN: [self.city],
            STATE_COLUMN: [self.state],
            ZIPCODE_COLUMN: [self.zipcode],
        }

        categorical_columns = [CITY_COLUMN, STATE_COLUMN, ZIPCODE_COLUMN]

        latitude = self.latitude
        if latitude is not None:
            data[ADDRESS_LATITUDE_COLUMN] = [latitude]
        longitude = self.longitude
        if longitude is not None:
            data[ADDRESS_LONGITUDE_COLUMN] = [longitude]
        housenumber = self.housenumber
        if housenumber is not None:
            data[ADDRESS_HOUSENUMBER_COLUMN] = [housenumber]
            categorical_columns.append(ADDRESS_HOUSENUMBER_COLUMN)

        weather = self.weather
        if weather is not None:
            weather_df = weather.to_frame()
            for column in weather_df.columns.values:
                data[column] = weather_df[column].to_list()

        df = pd.DataFrame(
            data={
                ADDRESS_COLUMN_SUFFIX + COLUMN_SEPARATOR + k: v for k, v in data.items()
            }
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = list(
            set(update_columns_list(categorical_columns, ADDRESS_COLUMN_SUFFIX))
        )
        return df

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Report any cache rules."""
        return {}
