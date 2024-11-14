"""AFL combined venue model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests_cache

from ...address_model import AddressModel
from ...venue_model import VenueModel


class AFLCombinedVenueModel(VenueModel):
    """AFL combined implementation of the venue model."""

    def __init__(
        self, session: requests_cache.CachedSession, venue_model: VenueModel
    ) -> None:
        super().__init__(session)
        self._venue_model = venue_model

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        return self._venue_model.identifier

    @property
    def name(self) -> str:
        """Return the venue name."""
        return self._venue_model.name

    @property
    def address(self) -> AddressModel | None:
        """Return the venue address."""
        return self._venue_model.address

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return AddressModel.urls_expire_after()
