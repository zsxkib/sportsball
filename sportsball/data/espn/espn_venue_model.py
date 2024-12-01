"""ESPN venue model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ..address_model import AddressModel
from ..google.google_address_model import GoogleAddressModel
from ..venue_model import VenueModel


class ESPNVenueModel(VenueModel):
    """ESPN implementation of the venue model."""

    def __init__(self, session: requests.Session, venue: Dict[str, Any]) -> None:
        super().__init__(session)
        self._identifier = venue["id"]
        self._name = venue["fullName"]
        venue_address = venue["address"]
        city = venue_address["city"]
        state = venue_address["state"]
        zipcode = venue_address["zipCode"]
        self._address = GoogleAddressModel(
            f"{self._name} - {city} - {state} - {zipcode}", session
        )
        self._grass = venue["grass"]
        self._indoor = venue["indoor"]

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the venue name."""
        return self._name

    @property
    def address(self) -> AddressModel | None:
        """Return the venue address."""
        return self._address

    @property
    def is_grass(self) -> bool | None:
        """Whether the venue has grass."""
        return self._grass

    @property
    def is_indoor(self) -> bool | None:
        """Whether the venue is indoor."""
        return self._indoor

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return AddressModel.urls_expire_after()
