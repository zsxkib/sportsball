"""The high PSI feature reducer."""

import pandas as pd
from feature_engine.selection import DropHighPSIFeatures

from .reducer import Reducer


class HighPSIReducer(Reducer):
    """The high PSI reducer class."""

    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        super().__init__()
        self._psi = DropHighPSIFeatures()

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the dataframe and remove the necessary features."""
        return self._psi.fit_transform(df)
