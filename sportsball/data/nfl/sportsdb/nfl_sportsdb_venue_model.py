"""NFL SportsDB venue model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ...address_model import AddressModel
from ...google.google_address_model import GoogleAddressModel
from ...venue_model import VenueModel


class NFLSportsDBVenueModel(VenueModel):
    """NFL SportsDB implementation of the venue model."""

    _sportsdb_address: AddressModel | None

    def __init__(
        self,
        session: requests.Session,
        dt: datetime.datetime,
        venue_id: str,
    ) -> None:
        super().__init__(session)
        if venue_id == "19533":
            venue_id = "17146"
        if venue_id == "21813":
            venue_id = "23848"
        if venue_id == "21642":
            venue_id = "29570"
        if venue_id == "23652":
            venue_id = "29569"
        if venue_id == "23654":
            venue_id = "15874"
        if venue_id == "23655":
            venue_id = "30856"
        if venue_id == "23656":
            venue_id = "29575"
        if venue_id == "23657":
            venue_id = "23720"
        response = session.get(
            f"https://www.thesportsdb.com/api/v1/json/3/lookupvenue.php?id={venue_id}"
        )
        response.raise_for_status()
        self._venue = response.json()["venues"][0]
        self._dt = dt
        self._sportsdb_address = None

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        return self._venue["idVenue"]

    @property
    def name(self) -> str:
        """Return the venue name."""
        return self._venue["strVenue"]

    @property
    def address(self) -> AddressModel | None:
        """Return the venue address."""
        address = self._sportsdb_address
        if address is None:
            # print(f"Getting address for venue ID {self.identifier}")
            address = GoogleAddressModel(
                " - ".join(
                    [
                        x
                        for x in [
                            self.name,
                            self._venue["strLocation"],
                            self._venue["strCountry"],
                        ]
                        if x is not None and x
                    ]
                ),
                self.session,
                self._dt,
            )
            self._sportsdb_address = address
        return address

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return GoogleAddressModel.urls_expire_after()
