"""The prototype class defining how to interface to the league."""

from typing import Iterator

import pandas as pd
import requests_cache

from .league import League
from .season_model import SeasonModel


class LeagueModel:
    """The prototype league model class."""

    def __init__(self, league: League, session: requests_cache.CachedSession) -> None:
        self._league = league
        self._session = session

    @property
    def session(self) -> requests_cache.CachedSession:
        """Return the cached session."""
        return self._session

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        """Find the seasons represented by the league."""
        raise NotImplementedError("season not implemented by LeagueModel parent class.")

    @property
    def league(self) -> League:
        """Return the league this league model represents."""
        return self._league

    def to_frame(self) -> pd.DataFrame:
        """Render the league as a dataframe."""
        dfs = [x.to_frame() for x in self.seasons]
        if not dfs:
            return pd.DataFrame()
        df = pd.concat(dfs)
        df["league"] = self.league.value
        return df
