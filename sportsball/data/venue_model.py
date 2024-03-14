"""The prototype class for a venue."""

import pandas as pd

from .address import Address


class VenueModel:
    """The prototype venue class."""

    def __init__(self, identifier: str, name: str, address: Address) -> None:
        self._identifier = identifier
        self._name = name
        self._address = address

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the venue name."""
        return self._name

    @property
    def address(self) -> Address:
        """Return the venue address."""
        return self._address

    def to_frame(self) -> pd.DataFrame:
        """Render the address's dataframe."""
        data = {
            "identifier": [self.identifier],
            "name": [self.name],
        }
        address_df = self.address.to_frame()
        for column in address_df.columns.values:
            data[column] = address_df[column].to_list()
        return pd.DataFrame(data={"venue_" + k: v for k, v in data.items()})
