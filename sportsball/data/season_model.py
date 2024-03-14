"""The prototype class for a season."""

from typing import Iterator

import pandas as pd
import requests_cache

from .game_model import GAME_COLUMN_SUFFIX, GAME_DT_COLUMN, GameModel
from .season_type import SeasonType


class SeasonModel:
    """The prototype class for a season."""

    def __init__(
        self, year: int, session: requests_cache.CachedSession, season_type: SeasonType
    ) -> None:
        self._year = year
        self._session = session
        self._season_type = season_type

    @property
    def year(self) -> int:
        """Return the year."""
        return self._year

    @property
    def session(self) -> requests_cache.CachedSession:
        """Return the cached session."""
        return self._session

    @property
    def season_type(self) -> SeasonType:
        """Return the season type."""
        return self._season_type

    @property
    def games(self) -> Iterator[GameModel]:
        """Find the games within the season."""
        raise NotImplementedError("games not implemented by SeasonModel parent class.")

    def to_frame(self) -> pd.DataFrame:
        """Render the season to a dataframe."""
        dfs = [x.to_frame() for x in self.games]
        if not dfs:
            return pd.DataFrame()
        df = pd.concat(dfs)
        df["season_type"] = self.season_type.value
        return df.sort_values(by=GAME_COLUMN_SUFFIX + GAME_DT_COLUMN, ascending=False)
