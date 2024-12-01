"""AFL combined player model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ...player_model import PlayerModel
from ..afltables.afl_afltables_player_model import AFLAFLTablesPlayerModel


class AFLCombinedPlayerModel(PlayerModel):
    """AFL combined implementation of the player model."""

    def __init__(
        self, session: requests.Session, player_models: list[PlayerModel]
    ) -> None:
        super().__init__(session)
        self._player_models = player_models

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._player_models[0].identifier

    @property
    def jersey(self) -> Optional[str]:
        """Return the jersey."""
        jersey = None
        for player_model in self._player_models:
            jersey = player_model.jersey
            if jersey is not None:
                break
        return jersey

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
