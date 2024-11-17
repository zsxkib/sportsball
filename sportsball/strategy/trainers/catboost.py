"""The catboost class for a trainer."""

import os
from typing import Any

import optuna
import pandas as pd
from catboost import CatBoostClassifier, Pool  # type: ignore

from .output_column import OUTPUT_COLUMN
from .trainer import Trainer

_MODEL_FILENAME = "model.cbm"


class CatboostTrainer(Trainer):
    """The catboost trainer class."""

    def __init__(
        self,
        folder: str,
        categorical_features: list[str],
        text_features: list[str],
        trial: optuna.trial.Trial | optuna.trial.FrozenTrial | None = None,
    ) -> None:
        super().__init__(folder)
        self._categorical_features = categorical_features
        self._text_features = text_features
        if trial is None:
            self._features_ratio = 0.0
            self._steps = 0
            self._model = CatBoostClassifier()
        else:
            self._features_ratio = trial.suggest_float("features_ratio", 0.1, 0.9)
            self._steps = trial.suggest_int("steps", 1, 10)
            self._model = CatBoostClassifier(
                iterations=trial.suggest_int("iterations", 100, 3000),
                learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
                depth=trial.suggest_int("depth", 3, 10),
                l2_leaf_reg=trial.suggest_float("l2_leaf_reg", 1.5, 4.5),
            )

    @property
    def clf(self) -> Any:
        """The underlying classifier"""
        return self._model

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        """Fit the data."""
        train_pool = self._create_pool(x, y)
        self._model.fit(train_pool)

    def save(self):
        """Save the trainer."""
        self._model.save_model(os.path.join(self._folder, _MODEL_FILENAME))

    def load(self):
        """Load the trainer."""
        self._model.load_model(os.path.join(self._folder, _MODEL_FILENAME))

    def predict(self, x: pd.DataFrame) -> pd.DataFrame | None:
        """Predict the Y values."""
        y = super().predict(x)
        if y is None:
            return y
        train_pool = self._create_pool(x, None)
        y = pd.DataFrame(
            index=x.index, data={OUTPUT_COLUMN: self._model.predict(train_pool)}
        )
        self.save_prediction(x, y)
        return y

    def select_features(self, x: pd.DataFrame, y: pd.DataFrame) -> list[str]:
        """Select the features from the training data."""
        train_pool = self._create_pool(x, y)
        summary = self._model.select_features(
            train_pool,
            num_features_to_select=int(self._features_ratio * len(x.columns.values)),
            steps=self._steps,
            train_final_model=False,
            features_for_select=x.columns.values,
        )
        return summary["selected_features_names"]

    def _create_pool(self, x: pd.DataFrame, y: pd.DataFrame | None) -> Pool:
        text_features = list(set(x.columns.values) & set(self._text_features))
        x[text_features] = x[text_features].fillna("").astype(str)
        cat_features = list(set(x.columns.values) & set(self._categorical_features))
        x[cat_features] = x[cat_features].fillna(0).astype(int)
        if y is not None:
            return Pool(
                x,
                y,
                cat_features=cat_features,
                text_features=text_features,
            )
        return Pool(
            x,
            cat_features=cat_features,
            text_features=text_features,
        )
