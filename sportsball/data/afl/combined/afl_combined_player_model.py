"""AFL combined player model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests_cache

from ...player_model import PlayerModel
from ..afltables.afl_afltables_player_model import AFLAFLTablesPlayerModel


class AFLCombinedPlayerModel(PlayerModel):
    """AFL combined implementation of the player model."""

    def __init__(
        self, session: requests_cache.CachedSession, player_model: PlayerModel
    ) -> None:
        super().__init__(session)
        self._player_model = player_model

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._player_model.identifier

    @property
    def jersey(self) -> Optional[str]:
        """Return the jersey."""
        return self._player_model.jersey

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **AFLAFLTablesPlayerModel.urls_expire_after(),
        }
