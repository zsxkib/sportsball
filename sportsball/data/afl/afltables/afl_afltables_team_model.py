"""AFL AFLTables team model."""

import datetime
import os
from typing import Any, Dict, Optional, Pattern, Sequence, Union
from urllib.parse import urlparse

import requests_cache
from bs4 import BeautifulSoup

from ...player_model import PlayerModel
from ...team_model import TeamModel
from .afl_afltables_player_model import AFLAFLTablesPlayerModel


class AFLAFLTablesTeamModel(TeamModel):
    """AFL AFLTables implementation of the team model."""

    def __init__(
        self,
        team_url: str,
        players: list[tuple[str, str, int | None]],
        points: float,
        session: requests_cache.CachedSession,
    ) -> None:
        super().__init__(session)
        response = session.get(team_url)
        soup = BeautifulSoup(response.text, "html.parser")
        self._players_info = players
        o = urlparse(team_url)
        last_component = o.path.split("/")[-1]
        self._identifier, _ = os.path.splitext(last_component)
        h1 = soup.find("h1")
        if h1 is None:
            raise ValueError("h1 is null.")
        self._name = h1.get_text()
        self._points = points
        self._players: Sequence[PlayerModel] = []

    @property
    def players(self) -> Sequence[PlayerModel]:
        if len(self._players) < len(self._players_info):
            self._players = [
                AFLAFLTablesPlayerModel(self.session, player_url, jersey, kicks)
                for player_url, jersey, kicks in self._players_info
            ]
        return self._players

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @property
    def points(self) -> float | None:
        """Return the points scored in the game."""
        return self._points

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
