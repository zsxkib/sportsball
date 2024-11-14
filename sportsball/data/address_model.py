"""A class for holding address information."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import pandas as pd
import requests_cache

from .columns import COLUMN_SEPARATOR
from .model import Model

ADDRESS_COLUMN_SUFFIX = "address"


class AddressModel(Model):
    """The class for representing an address."""

    def __init__(
        self, session: requests_cache.CachedSession, city: str, state: str, zipcode: str
    ) -> None:
        super().__init__(session)
        self._city = city
        self._state = state
        self._zipcode = zipcode

    @property
    def city(self) -> str:
        """Return the city."""
        return self._city

    @property
    def state(self) -> str:
        """Return the state."""
        return self._state

    @property
    def zipcode(self) -> str:
        """Return the zipcode."""
        return self._zipcode

    def to_frame(self) -> pd.DataFrame:
        """Render the address as a dataframe."""
        data = {
            "city": [self.city],
            "state": [self.state],
            "zipcode": [self.zipcode],
        }
        return pd.DataFrame(
            data={
                ADDRESS_COLUMN_SUFFIX + COLUMN_SEPARATOR + k: v for k, v in data.items()
            }
        )

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Report any cache rules."""
        return {}
