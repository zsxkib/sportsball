"""NFL player model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...player_model import PlayerModel


class NFLESPNPlayerModel(PlayerModel):
    """NFL implementation of the player model."""

    def __init__(self, player: Dict[str, Any]) -> None:
        identifier = str(player["playerId"])
        jersey = player.get("jersey")
        super().__init__(identifier, jersey)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
