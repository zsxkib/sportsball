"""The prototype class defining how to interface to the league."""

from typing import Iterator

import pandas as pd
import requests
import tqdm

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      ODDS_COLUMNS_ATTR, POINTS_COLUMNS_ATTR,
                      TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR)
from .game_model import GAME_COLUMN_PREFIX, GAME_DT_COLUMN
from .league import League
from .model import Model
from .season_model import SeasonModel

LEAGUE_COLUMN = "league"


class LeagueModel(Model):
    """The prototype league model class."""

    _df: pd.DataFrame | None

    def __init__(self, league: League, session: requests.Session) -> None:
        super().__init__(session)
        self._league = league
        self._df = None

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
        df = self._df
        if df is None:
            dfs = [x.to_frame() for x in tqdm.tqdm(self.seasons, desc="Seasons")]
            if not dfs:
                return pd.DataFrame()
            df = pd.concat(dfs)
            df[LEAGUE_COLUMN] = self.league.value
            df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = [LEAGUE_COLUMN]
            df.attrs[ODDS_COLUMNS_ATTR] = []
            df.attrs[POINTS_COLUMNS_ATTR] = []
            df.attrs[TEXT_COLUMNS_ATTR] = []
            df.attrs[CATEGORICAL_COLUMNS_ATTR] = [LEAGUE_COLUMN]
            for season_df in dfs:
                df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR].extend(
                    season_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, [])
                )
                df.attrs[ODDS_COLUMNS_ATTR].extend(
                    season_df.attrs.get(ODDS_COLUMNS_ATTR, [])
                )
                df.attrs[POINTS_COLUMNS_ATTR].extend(
                    season_df.attrs.get(POINTS_COLUMNS_ATTR, [])
                )
                df.attrs[TEXT_COLUMNS_ATTR].extend(
                    season_df.attrs.get(TEXT_COLUMNS_ATTR, [])
                )
                df.attrs[CATEGORICAL_COLUMNS_ATTR].extend(
                    season_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, [])
                )
            df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
                set(df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR])
            )
            df.attrs[ODDS_COLUMNS_ATTR] = sorted(list(set(df.attrs[ODDS_COLUMNS_ATTR])))
            df.attrs[POINTS_COLUMNS_ATTR] = sorted(
                list(set(df.attrs[POINTS_COLUMNS_ATTR]))
            )
            df.attrs[TEXT_COLUMNS_ATTR] = sorted(list(set(df.attrs[TEXT_COLUMNS_ATTR])))
            df.attrs[CATEGORICAL_COLUMNS_ATTR] = sorted(
                list(set(df.attrs[CATEGORICAL_COLUMNS_ATTR]))
            )

            for categorical_column in df.attrs[CATEGORICAL_COLUMNS_ATTR]:
                df[categorical_column] = df[categorical_column].astype("category")
            df = df.sort_values(
                by=COLUMN_SEPARATOR.join([GAME_COLUMN_PREFIX, GAME_DT_COLUMN]),
                ascending=True,
            )

            self._df = df
        return df
