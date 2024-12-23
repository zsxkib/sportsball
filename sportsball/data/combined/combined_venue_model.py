"""Combined venue model."""

import datetime

import requests

from ..address_model import AddressModel
from ..venue_model import VenueModel


class CombinedVenueModel(VenueModel):
    """Combined implementation of the venue model."""

    _address: AddressModel | None

    def __init__(
        self,
        session: requests.Session,
        venue_models: list[VenueModel],
        dt: datetime.datetime,
    ) -> None:
        super().__init__(session)
        self._venue_models = venue_models
        self._address = None
        self._dt = dt

    @classmethod
    def venue_identity_map(cls) -> dict[str, str]:
        """The mapping of all the venue identities."""
        raise NotImplementedError("venue_identity_map not implemented on parent class.")

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        return self.venue_identity_map()[self._venue_models[0].identifier]

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
            self._address = address
        return address
