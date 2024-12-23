"""AFL AFLTables venue model."""

import datetime
import os
from typing import Any, Dict, Optional, Pattern, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from ...address_model import AddressModel
from ...google.google_address_model import GoogleAddressModel
from ...venue_model import VenueModel


class AFLAFLTablesVenueModel(VenueModel):
    """AFL AFLTables implementation of the venue model."""

    _address: AddressModel | None

    def __init__(
        self, url: str, session: requests.Session, dt: datetime.datetime
    ) -> None:
        super().__init__(session)
        o = urlparse(url)
        last_component = o.path.split("/")[-1]
        self._identifier, _ = os.path.splitext(last_component)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        name = None
        for h1 in soup.find_all("h1"):
            name = h1.get_text()
        if name is None:
            raise ValueError("name is null.")
        self._name = name
        self._address = None
        self._dt = dt

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
        address = self._address
        if address is None:
            address = GoogleAddressModel(
                f"{self.name} - Australia", self.session, self._dt
            )
            self._address = address
        return address

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return AddressModel.urls_expire_after()
