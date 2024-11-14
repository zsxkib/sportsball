"""AFL AFLTables venue model."""

import datetime
import os
from typing import Any, Dict, Optional, Pattern, Union
from urllib.parse import urlparse

import requests_cache
from bs4 import BeautifulSoup

from ...address_model import AddressModel
from ...venue_model import VenueModel


class AFLAFLTablesVenueModel(VenueModel):
    """AFL AFLTables implementation of the venue model."""

    def __init__(self, url: str, session: requests_cache.CachedSession) -> None:
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

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the venue name."""
        return self._name

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return AddressModel.urls_expire_after()
