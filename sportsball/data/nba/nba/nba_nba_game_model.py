"""NBA NBA game model."""
# pylint: disable=abstract-method

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...game_model import GameModel


class NBANBAGameModel(GameModel):
    """NBA NBA implementation of the game model."""

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            # **ESPNVenueModel.urls_expire_after(),
            # **ESPNTeamModel.urls_expire_after(),
        }
