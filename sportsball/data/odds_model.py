"""The prototype class for odds."""

import pandas as pd

from .bookie_model import BookieModel


class OddsModel:
    """The prototype odds class."""

    def __init__(self, odds: float, bookie: BookieModel) -> None:
        self._odds = odds
        self._bookie = bookie

    @property
    def odds(self) -> float:
        """Return the odds."""
        return self._odds

    @property
    def bookie(self) -> BookieModel:
        """Return the bookie."""
        return self._bookie

    def to_frame(self) -> pd.DataFrame:
        """Render the odds as a dataframe."""
        data = {
            "odds": [self.odds],
        }

        bookie_df = self.bookie.to_frame()
        for column in bookie_df.columns.values:
            data[column] = bookie_df[column].to_list()

        return pd.DataFrame(data={"odds_" + k: v for k, v in data.items()})
