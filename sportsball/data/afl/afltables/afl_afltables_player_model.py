"""AFL AFLTables player model."""

import datetime
import os
from typing import Any, Dict, Optional, Pattern, Union
from urllib.parse import urlparse

import requests_cache

from ...player_model import PlayerModel


class AFLAFLTablesPlayerModel(PlayerModel):
    """AFL AFLTables implementation of the player model."""

    def __init__(
        self, session: requests_cache.CachedSession, player_url: str, jersey: str
    ) -> None:
        super().__init__(session)
        o = urlparse(player_url)
        last_component = o.path.split("/")[-1]
        self._identifier, _ = os.path.splitext(last_component)
        self._jersey = "".join(filter(str.isdigit, jersey))

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
