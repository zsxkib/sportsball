"""Google address model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import geocoder  # type: ignore
import requests_cache

from ..address_model import AddressModel


class GoogleAddressModel(AddressModel):
    """Google implementation of the address model."""

    def __init__(self, query: str, session: requests_cache.CachedSession) -> None:
        g = geocoder.google(query, session=session)
        super().__init__(session, g.city, g.state, g.postal)
        self._latitude = g.lat
        self._longitude = g.lng

    @property
    def latitude(self) -> float | None:
        """Return the latitude."""
        return self._latitude

    @property
    def longitude(self) -> float | None:
        """Return the longitude."""
        return self._longitude

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
