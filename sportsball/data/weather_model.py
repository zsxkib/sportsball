"""A class for holding weather information."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import pandas as pd

from .columns import COLUMN_SEPARATOR
from .model import Model

WEATHER_COLUMN_PREFIX = "weather"
WEATHER_COLUMN_TEMPERATURE = "temperature"


class WeatherModel(Model):
    """The class for representing weather."""

    @property
    def temperature(self) -> float | None:
        """Return the temperature."""
        raise NotImplementedError("temperature is not implemented in parent class.")

    def to_frame(self) -> pd.DataFrame:
        """Render the address as a dataframe."""
        data: dict[str, list[float]] = {}

        temperature = self.temperature
        if temperature is not None:
            data[WEATHER_COLUMN_TEMPERATURE] = [temperature]

        df = pd.DataFrame(
            data={
                WEATHER_COLUMN_PREFIX + COLUMN_SEPARATOR + k: v for k, v in data.items()
            }
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
