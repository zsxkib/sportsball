"""The prototype class for odds."""

import pandas as pd

from .bookie_model import BookieModel
from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      ODDS_COLUMNS_ATTR, POINTS_COLUMNS_ATTR,
                      TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR,
                      update_columns_list)
from .model import Model

ODDS_COLUMN_SUFFIX = "odds"
ODDS_ODDS_COLUMN = "odds"


class OddsModel(Model):
    """The prototype odds class."""

    @property
    def odds(self) -> float:
        """Return the odds."""
        raise NotImplementedError("odds not implemented in parent class.")

    @property
    def bookie(self) -> BookieModel:
        """Return the bookie."""
        raise NotImplementedError("bookie not implemented in parent class.")

    def to_frame(self) -> pd.DataFrame:
        """Render the odds as a dataframe."""
        data = {
            ODDS_ODDS_COLUMN: [self.odds],
        }

        bookie_df = self.bookie.to_frame()
        training_exclude_columns = bookie_df.attrs.get(
            TRAINING_EXCLUDE_COLUMNS_ATTR, []
        )
        odds_columns = bookie_df.attrs.get(ODDS_COLUMNS_ATTR, [])
        odds_columns.append(ODDS_ODDS_COLUMN)
        points_columns = bookie_df.attrs.get(POINTS_COLUMNS_ATTR, [])
        text_columns = bookie_df.attrs.get(TEXT_COLUMNS_ATTR, [])
        categorical_columns = bookie_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, [])

        for column in bookie_df.columns.values:
            data[column] = bookie_df[column].to_list()

        df = pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([ODDS_COLUMN_SUFFIX, k]): v
                for k, v in data.items()
            }
        )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(update_columns_list(training_exclude_columns, ODDS_COLUMN_SUFFIX))
        )
        df.attrs[ODDS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(odds_columns, ODDS_COLUMN_SUFFIX)))
        )
        df.attrs[POINTS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(points_columns, ODDS_COLUMN_SUFFIX)))
        )
        df.attrs[TEXT_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(text_columns, ODDS_COLUMN_SUFFIX)))
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(categorical_columns, ODDS_COLUMN_SUFFIX)))
        )
        return df
