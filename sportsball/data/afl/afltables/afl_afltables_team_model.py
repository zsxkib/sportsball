"""AFL AFLTables team model."""

# pylint: disable=too-many-arguments
import datetime
import os
from typing import Any, Dict, Optional, Pattern, Sequence, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from ...player_model import PlayerModel
from ...team_model import TeamModel
from .afl_afltables_player_model import AFLAFLTablesPlayerModel

_TEAM_NAME_MAP = {
    "Melbourne": ["ME"],
    "Geelong": ["GE"],
    "Fitzroy": ["FI"],
    "Collingwood": ["CW"],
    "Essendon": ["ES"],
    "South Melbourne": ["SM"],
    "St Kilda": ["SK"],
    "Carlton": ["CA"],
    "Sydney": ["SM", "SY"],
    "University": ["UN"],
    "Richmond": ["RI"],
    "North Melbourne": ["NM"],
    "Western Bulldogs": ["WB", "FO"],
    "Hawthorn": ["HW"],
    "Brisbane Bears": ["BB"],
    "West Coast": ["WC"],
    "Adelaide": ["AD"],
    "Fremantle": ["FR"],
    "Brisbane Lions": ["BL"],
    "Port Adelaide": ["PA"],
    "Gold Coast": ["GC"],
    "Greater Western Sydney": ["GW"],
}


class AFLAFLTablesTeamModel(TeamModel):
    """AFL AFLTables implementation of the team model."""

    def __init__(
        self,
        team_url: str,
        players: list[tuple[str, str, int | None]],
        points: float,
        session: requests.Session,
        last_ladder_ranks: dict[str, int] | None,
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
        self._last_ladder_rank = None
        if last_ladder_ranks is not None and last_ladder_ranks:
            short_names = _TEAM_NAME_MAP[self._name]
            for short_name in short_names:
                if short_name in last_ladder_ranks:
                    self._last_ladder_rank = last_ladder_ranks[short_name]
                    break

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

    @property
    def ladder_rank(self) -> int | None:
        """Return the ladder rank for this team."""
        return self._last_ladder_rank

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
