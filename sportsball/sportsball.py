"""The main sportsball class for accessing data."""

import datetime
from typing import Dict
from warnings import simplefilter

import pandas as pd
import requests
import requests_cache
from dotenv import load_dotenv
from retry_requests import retry  # type: ignore

from .data.afl import AFLLeagueModel
from .data.league import League
from .data.league_model import LeagueModel
from .data.nba import NBALeagueModel
from .data.ncaab import NCAABLeagueModel
from .data.ncaaf import NCAAFLeagueModel
from .data.nfl import NFLLeagueModel
from .portfolio import Portfolio
from .strategy import Strategy


class SportsBall:
    """The main sportsball class."""

    _leagues: Dict[str, LeagueModel]
    _session: requests.Session

    def __init__(self) -> None:
        cache_session = requests_cache.CachedSession(
            "sportsball",
            expire_after=datetime.timedelta(days=365),
        )
        self._session = retry(cache_session, retries=5, backoff_factor=0.2)
        self._leagues = {}
        simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
        load_dotenv()

    def league(self, league: League) -> LeagueModel:
        """Provide a league model for the given league."""
        if league not in self._leagues:
            if league == League.NFL:
                self._leagues[league] = NFLLeagueModel(self._session)
            elif league == League.AFL:
                self._leagues[league] = AFLLeagueModel(self._session)
            elif league == League.NBA:
                self._leagues[league] = NBALeagueModel(self._session)
            elif league == League.NCAAF:
                self._leagues[league] = NCAAFLeagueModel(self._session)
            elif league == League.NCAAB:
                self._leagues[league] = NCAABLeagueModel(self._session)
            else:
                raise ValueError(f"Unrecognised league: {league}")
        return self._leagues[league]

    def create_strategy(self, league: LeagueModel, name: str) -> Strategy:
        """Creates a strategy."""
        return Strategy(league.to_frame(), name)

    def create_portfolio(self, strategies: list[Strategy], name: str) -> Portfolio:
        """Creates a portfolio."""
        return Portfolio(strategies, name)
