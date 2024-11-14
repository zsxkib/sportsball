"""AFL aussportsbetting bookie model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...bookie_model import BookieModel


class AFLAusSportsBettingBookieModel(BookieModel):
    """AFL AusSportsBetting implementation of the bookie model."""

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return "bet365"

    @property
    def name(self) -> str:
        """Return the name."""
        return "Bet365"

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
