"""NFL bookie model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ..bookie_model import BookieModel


class NFLBookieModel(BookieModel):
    """NFL implementation of the bookie model."""

    def __init__(self, bookie: Dict[str, Any]) -> None:
        identifier = bookie["id"]
        name = bookie["name"]
        super().__init__(identifier, name)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
