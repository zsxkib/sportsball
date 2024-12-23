"""NFL combined player model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...combined.combined_player_model import CombinedPlayerModel
from ..espn.nfl_espn_player_model import NFLESPNPlayerModel


class NFLCombinedPlayerModel(CombinedPlayerModel):
    """NFL combined implementation of the player model."""

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **NFLESPNPlayerModel.urls_expire_after(),
        }
