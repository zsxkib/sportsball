"""AFL combined venue model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests_cache

from ...address_model import AddressModel
from ...google.google_address_model import GoogleAddressModel
from ...venue_model import VenueModel


class AFLCombinedVenueModel(VenueModel):
    """AFL combined implementation of the venue model."""

    _address: AddressModel | None

    def __init__(
        self, session: requests_cache.CachedSession, venue_models: list[VenueModel]
    ) -> None:
        super().__init__(session)
        self._venue_models = venue_models
        self._address = None

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        return self._venue_models[0].identifier

    @property
    def name(self) -> str:
        """Return the venue name."""
        return self._venue_models[0].name

    @property
    def address(self) -> AddressModel | None:
        """Return the venue address."""
        address = self._address
        if address is None:
            for venue_model in self._venue_models:
                address = venue_model.address
                if address is not None:
                    break
            if address is None:
                address = GoogleAddressModel(f"{self.name} - Australia", self._session)
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
