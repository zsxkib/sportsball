"""Google address model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import geocoder  # type: ignore
import requests

from ..address_model import AddressModel
from ..openmeteo.openmeteo_weather_model import OpenmeteoWeatherModel
from ..weather_model import WeatherModel

_CACHED_GEOCODES: dict[str, Any] = {}


class GoogleAddressModel(AddressModel):
    """Google implementation of the address model."""

    def __init__(
        self, query: str, session: requests.Session, dt: datetime.datetime
    ) -> None:
        g = _CACHED_GEOCODES.get(query)
        if g is None:
            g = geocoder.google(query, session=session)
            _CACHED_GEOCODES[query] = g
        super().__init__(session, g.city, g.state, g.postal)
        self._latitude = g.lat
        self._longitude = g.lng
        self._housenumber = g.housenumber
        self._dt = dt

    @property
    def latitude(self) -> float | None:
        """Return the latitude."""
        return self._latitude

    @property
    def longitude(self) -> float | None:
        """Return the longitude."""
        return self._longitude

    @property
    def housenumber(self) -> str | None:
        """Return the housenumber."""
        return self._housenumber

    @property
    def weather(self) -> WeatherModel | None:
        """Return the weather."""
        latitude = self._latitude
        longitude = self._longitude
        if latitude is None or longitude is None:
            return None
        return OpenmeteoWeatherModel(
            self.session, self._latitude, self._longitude, self._dt
        )

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
