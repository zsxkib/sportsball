"""NFL venue model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...address import Address
from ...venue_model import VenueModel


class NFLESPNVenueModel(VenueModel):
    """NFL implementation of the venue model."""

    def __init__(self, venue: Dict[str, Any]) -> None:
        identifier = venue["id"]
        name = venue["fullName"]
        venue_address = venue["address"]
        city = venue_address["city"]
        state = venue_address["state"]
        zipcode = venue_address["zipCode"]
        address = Address(city, state, zipcode)
        super().__init__(identifier, name, address)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return Address.urls_expire_after()
