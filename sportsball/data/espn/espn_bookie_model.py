"""ESPN bookie model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ..bookie_model import BookieModel


class ESPNBookieModel(BookieModel):
    """ESPN implementation of the bookie model."""

    def __init__(self, session: requests.Session, bookie: Dict[str, Any]) -> None:
        super().__init__(session)
        self._identifier = bookie["id"]
        self._name = bookie["name"]

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
