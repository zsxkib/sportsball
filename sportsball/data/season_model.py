"""The prototype class for a season."""

from typing import Iterator

import pandas as pd
import tqdm

from .columns import (COLUMN_SEPARATOR, ODDS_COLUMNS_ATTR,
                      TRAINING_EXCLUDE_COLUMNS_ATTR)
from .game_model import GAME_COLUMN_SUFFIX, GAME_DT_COLUMN, GameModel
from .model import Model
from .season_type import SeasonType


class SeasonModel(Model):
    """The prototype class for a season."""

    @property
    def year(self) -> int | None:
        """Return the year."""
        raise NotImplementedError("year not implemented by parent class.")

    @property
    def season_type(self) -> SeasonType | None:
        """Return the season type."""
        raise NotImplementedError("season_type not implemented by parent class.")

    @property
    def games(self) -> Iterator[GameModel]:
        """Find the games within the season."""
        raise NotImplementedError("games not implemented by SeasonModel parent class.")

    def to_frame(self) -> pd.DataFrame:
        """Render the season to a dataframe."""
        dfs = [x.to_frame() for x in tqdm.tqdm(self.games, desc="Games")]
        if not dfs:
            return pd.DataFrame()
        df = pd.concat(dfs)
        season_type = self.season_type
        if season_type is not None:
            df["season_type"] = season_type.value
        year = self.year
        if year is not None:
            df["year"] = year
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = []
        df.attrs[ODDS_COLUMNS_ATTR] = []
        for game_df in dfs:
            df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR].extend(
                game_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, [])
            )
            df.attrs[ODDS_COLUMNS_ATTR].extend(game_df.attrs.get(ODDS_COLUMNS_ATTR, []))
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR])
        )
        df.attrs[ODDS_COLUMNS_ATTR] = sorted(list(set(df.attrs[ODDS_COLUMNS_ATTR])))
        return df.sort_values(
            by=COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN]),
            ascending=False,
        )
