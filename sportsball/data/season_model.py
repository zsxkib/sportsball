"""The prototype class for a season."""

from typing import Iterator

import pandas as pd
import tqdm

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      ODDS_COLUMNS_ATTR, POINTS_COLUMNS_ATTR,
                      TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR)
from .game_model import GAME_COLUMN_PREFIX, GAME_DT_COLUMN, GameModel
from .model import Model
from .season_type import SeasonType

SEASON_TYPE_COLUMN = "season_type"
SEASON_YEAR_COLUMN = "year"


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
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = []
        df.attrs[ODDS_COLUMNS_ATTR] = []
        df.attrs[POINTS_COLUMNS_ATTR] = []
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = []
        df.attrs[TEXT_COLUMNS_ATTR] = []

        season_type = self.season_type
        if season_type is not None:
            df[SEASON_TYPE_COLUMN] = season_type.value
            df.attrs[CATEGORICAL_COLUMNS_ATTR].append(SEASON_TYPE_COLUMN)

        year = self.year
        if year is not None:
            df[SEASON_YEAR_COLUMN] = year

        for game_df in dfs:
            df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR].extend(
                game_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, [])
            )
            df.attrs[ODDS_COLUMNS_ATTR].extend(game_df.attrs.get(ODDS_COLUMNS_ATTR, []))
            df.attrs[POINTS_COLUMNS_ATTR].extend(
                game_df.attrs.get(POINTS_COLUMNS_ATTR, [])
            )
            df.attrs[TEXT_COLUMNS_ATTR].extend(game_df.attrs.get(TEXT_COLUMNS_ATTR, []))
            df.attrs[CATEGORICAL_COLUMNS_ATTR].extend(
                game_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, [])
            )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR])
        )
        df.attrs[ODDS_COLUMNS_ATTR] = sorted(list(set(df.attrs[ODDS_COLUMNS_ATTR])))
        df.attrs[POINTS_COLUMNS_ATTR] = sorted(list(set(df.attrs[POINTS_COLUMNS_ATTR])))
        df.attrs[TEXT_COLUMNS_ATTR] = sorted(list(set(df.attrs[TEXT_COLUMNS_ATTR])))
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = sorted(
            list(set(df.attrs[CATEGORICAL_COLUMNS_ATTR]))
        )
        return df.sort_values(
            by=COLUMN_SEPARATOR.join([GAME_COLUMN_PREFIX, GAME_DT_COLUMN]),
            ascending=False,
        )
