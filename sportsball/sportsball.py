"""The main sportsball class for accessing data."""

# pylint: disable=too-few-public-methods
import datetime
from typing import Dict

import requests_cache

from .data.league import League
from .data.league_model import LeagueModel
from .data.nfl.nfl_league_model import NFLLeagueModel


class SportsBall:
    """The main sportsball class."""

    _leagues: Dict[str, LeagueModel]

    def __init__(self) -> None:
        self._session = requests_cache.CachedSession(
            "sportsball",
            expire_after=datetime.timedelta(days=365),
            urls_expire_after=NFLLeagueModel.urls_expire_after(),
        )
        self._leagues = {}

    def league(self, league: League) -> LeagueModel:
        """Provide a league model for the given league."""
        if league not in self._leagues:
            if league == League.NFL:
                self._leagues[league] = NFLLeagueModel(self._session)
            else:
                raise ValueError(f"Unrecognised league: {league}")
        return self._leagues[league]
