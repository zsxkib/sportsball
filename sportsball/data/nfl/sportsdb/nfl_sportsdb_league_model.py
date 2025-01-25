"""NFL Sports DB league model."""

import requests_cache

from ...league import League
from ...sportsdb.sportsdb_league_model import SportsDBLeagueModel


class NFLSportsDBLeagueModel(SportsDBLeagueModel):
    """NFL SportsDB implementation of the league model."""

    def __init__(self, session: requests_cache.CachedSession) -> None:
        super().__init__(session, "4391", League.NFL)
