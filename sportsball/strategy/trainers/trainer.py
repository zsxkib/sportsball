"""The prototype class for a trainer."""

import hashlib
import os
from typing import Any

import pandas as pd


def _hash_df(df: pd.DataFrame) -> int:
    return int(
        hashlib.sha256(
            pd.util.hash_pandas_object(df, index=True).values,  # type: ignore
        ).hexdigest(),
        16,
    )


class Trainer:
    """The prototype trainer class."""

    def __init__(self, folder: str) -> None:
        self._folder = folder

    @property
    def clf(self) -> Any:
        """The underlying classifier"""
        raise NotImplementedError("clf is not implemented in parent class.")

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        """Fit the data."""
        raise NotImplementedError("fit is not implemented in parent class.")

    def save(self):
        """Save the trainer."""
        raise NotImplementedError("save is not implemented in parent class.")

    def load(self):
        """Load the trainer."""
        raise NotImplementedError("load is not implemented in parent class.")

    def predict(self, x: pd.DataFrame) -> pd.DataFrame | None:
        """Predict the Y values."""
        filename = os.path.join(self._folder, f"{_hash_df(x)}.parquet")
        if os.path.exists(filename):
            return pd.read_parquet(filename)
        return None

    def save_prediction(self, x: pd.DataFrame, y: pd.DataFrame):
        """Save the prediction for later."""
        filename = os.path.join(self._folder, f"{_hash_df(x)}.parquet")
        y.to_parquet(filename)

    def select_features(self, x: pd.DataFrame, y: pd.DataFrame) -> list[str]:
        """Select the features from the training data."""
        raise NotImplementedError("select_features is not implemented in parent class.")
