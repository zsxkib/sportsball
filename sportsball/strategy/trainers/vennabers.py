"""The vennabers class for a trainer."""

import os
from typing import Any

import joblib  # type: ignore
import pandas as pd
from venn_abers import VennAbersCalibrator  # type: ignore

from .output_column import OUTPUT_COLUMN, OUTPUT_PROB_COLUMN
from .trainer import Trainer

_MODEL_FILENAME = "va.sav"


class VennAbersTrainer(Trainer):
    """The catboost trainer class."""

    def __init__(self, folder: str, wrapped_trainer: Trainer) -> None:
        super().__init__(folder)
        self._wrapped_trainer = wrapped_trainer
        self._model = VennAbersCalibrator(
            estimator=wrapped_trainer.clf,
            inductive=True,
            cal_size=0.2,
            random_state=101,
        )

    @property
    def clf(self) -> Any:
        """The underlying classifier"""
        return self._model

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        """Fit the data."""
        self._model.fit(x, y)

    def save(self):
        """Save the trainer."""
        self._wrapped_trainer.save()
        joblib.dump(self._model, os.path.join(self._folder, _MODEL_FILENAME))

    def load(self):
        """Load the trainer."""
        self._wrapped_trainer.load()
        self._model = joblib.load(os.path.join(self._folder, _MODEL_FILENAME))

    def predict(self, x: pd.DataFrame) -> pd.DataFrame | None:
        """Predict the Y values."""
        y = super().predict(x)
        if y is None:
            return y
        y = pd.DataFrame(
            index=x.index,
            data={
                OUTPUT_COLUMN: self._model.predict(x),
                OUTPUT_PROB_COLUMN: self._model.predict_proba(x),
            },
        )
        self.save_prediction(x, y)
        return y

    def select_features(self, x: pd.DataFrame, y: pd.DataFrame) -> list[str]:
        """Select the features from the training data."""
        return self._wrapped_trainer.select_features(x, y)
