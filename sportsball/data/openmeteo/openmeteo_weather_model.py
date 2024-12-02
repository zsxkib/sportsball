"""Openmeteo weather model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import openmeteo_requests  # type: ignore
import pandas as pd
import requests
from tzwhere import tzwhere  # type: ignore

from ..weather_model import WeatherModel


class OpenmeteoWeatherModel(WeatherModel):
    """Google implementation of the address model."""

    def __init__(
        self,
        session: requests.Session,
        latitude: float,
        longitude: float,
        dt: datetime.datetime,
    ) -> None:
        super().__init__(session)
        print(f"latitude: {latitude}")
        print(f"longitude: {longitude}")
        client = openmeteo_requests.Client(session=session)
        tz = tzwhere.tzwhere()
        responses = client.weather_api(
            "https://archive-api.open-meteo.com/v1/archive",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": str((dt - datetime.timedelta(days=1.0)).date()),
                "end_date": str(dt.date()),
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "dew_point_2m",
                    "apparent_temperature",
                    "precipitation",
                    "rain",
                    "snowfall",
                    "snow_depth",
                    "weather_code",
                    "pressure_msl",
                    "surface_pressure",
                    "cloud_cover",
                    "cloud_cover_low",
                    "cloud_cover_mid",
                    "cloud_cover_high",
                    "et0_fao_evapotranspiration",
                    "vapour_pressure_deficit",
                    "wind_speed_10m",
                    "wind_speed_100m",
                    "wind_direction_10m",
                    "wind_direction_100m",
                    "wind_gusts_10m",
                    "soil_temperature_0_to_7cm",
                    "soil_temperature_7_to_28cm",
                    "soil_temperature_28_to_100cm",
                    "soil_temperature_100_to_255cm",
                    "soil_moisture_0_to_7cm",
                    "soil_moisture_7_to_28cm",
                    "soil_moisture_28_to_100cm",
                    "soil_moisture_100_to_255cm",
                ],
                "daily": [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "temperature_2m_mean",
                    "apparent_temperature_max",
                    "apparent_temperature_min",
                    "apparent_temperature_mean",
                    "sunrise",
                    "sunset",
                    "daylight_duration",
                    "sunshine_duration",
                    "precipitation_sum",
                    "rain_sum",
                    "snowfall_sum",
                    "precipitation_hours",
                    "wind_speed_10m_max",
                    "wind_gusts_10m_max",
                    "wind_direction_10m_dominant",
                    "shortwave_radiation_sum",
                    "et0_fao_evapotranspiration",
                ],
                "timezone": tz.tzNameAt(latitude, longitude),
            },
        )
        response = responses[0]
        hourly = response.Hourly()
        if hourly is None:
            raise ValueError("hourly is null.")
        hourly_df = pd.DataFrame(
            data={
                "date": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s"),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left",
                )
            }
        )
        hourly_idx = hourly_df.index.get_loc(dt, method="nearest")
        self._temperature = hourly_idx.iloc[hourly_idx]["temperature_2m"]  # type: ignore

    @property
    def temperature(self) -> float:
        """Return the temperature."""
        return self._temperature

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
