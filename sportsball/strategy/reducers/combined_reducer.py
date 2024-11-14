"""A feature reducer combining many sub feature reducers."""

import pandas as pd

from .constant_reducer import ConstantReducer
from .correlation_reducer import CorrelationReducer
from .duplicate_reducer import DuplicateReducer
from .highpsi_reducer import HighPSIReducer
from .reducer import Reducer


class CombinedReducer(Reducer):
    """Combined reducer extractor class."""

    # pylint: disable=too-few-public-methods

    def __init__(self, reducers: list[Reducer] | None = None) -> None:
        super().__init__()
        if reducers is None:
            reducers = [
                ConstantReducer(),
                DuplicateReducer(),
                CorrelationReducer(),
                HighPSIReducer(),
            ]
        self._reducers = reducers

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        for reducer in self._reducers:
            df = reducer.process(df)
        return df
