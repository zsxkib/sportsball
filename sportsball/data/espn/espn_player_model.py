"""ESPN player model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ..player_model import PlayerModel


class ESPNPlayerModel(PlayerModel):
    """ESPN implementation of the player model."""

    def __init__(self, session: requests.Session, player: Dict[str, Any]) -> None:
        super().__init__(session)
        self._identifier = str(player["playerId"])
        self._jersey = player.get("jersey")

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def jersey(self) -> Optional[str]:
        """Return the jersey."""
        return self._jersey

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {}
