"""The strategy class."""

import datetime
import os
import pickle
import statistics

import numpy as np
import optuna
import pandas as pd
from sklearn.metrics import accuracy_score  # type: ignore

from ..data.columns import (COLUMN_SEPARATOR, ODDS_COLUMNS_ATTR,
                            TRAINING_EXCLUDE_COLUMNS_ATTR)
from ..data.game_model import (GAME_COLUMN_SUFFIX, GAME_DT_COLUMN,
                               GAME_WEEK_COLUMN)
from .features import CombinedFeature
from .reducers import CombinedReducer
from .trainers import CatboostTrainer, VennAbersTrainer
from .trainers.output_column import OUTPUT_COLUMN, OUTPUT_PROB_COLUMN

_SAMPLER_FILENAME = "sampler.pkl"


def _next_week_dt(
    current_dt: datetime.datetime | None, df: pd.DataFrame
) -> datetime.datetime:
    week_column = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_WEEK_COLUMN])
    dt_column = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN])
    if current_dt is not None:
        df = df[df[dt_column] >= current_dt]
    current_week = df.iloc[0][week_column]
    for _, row in df.iterrows():
        week = row[week_column]
        if current_week != week:
            return pd.to_datetime(row[dt_column]).to_pydatetime()[0]
    return pd.to_datetime(df[dt_column]).to_pydatetime()[-1]  # type: ignore


class Strategy:
    """The strategy class."""

    # pylint: disable=too-many-locals

    def __init__(self, df: pd.DataFrame, name: str) -> None:
        self._df = df
        self._name = name
        self._features = CombinedFeature()
        self._reducers = CombinedReducer()
        os.makedirs(name, exist_ok=True)
        storage_name = f"sqlite:///{name}/study.db"
        sampler_file = os.path.join(name, _SAMPLER_FILENAME)
        restored_sampler = None
        if os.path.exists(sampler_file):
            with open(sampler_file, "rb") as handle:
                restored_sampler = pickle.load(handle)
        self._study = optuna.create_study(
            study_name=name,
            storage=storage_name,
            load_if_exists=True,
            sampler=restored_sampler,
        )

    def fit(self, start_dt: datetime.datetime | None = None):
        """Fits the strategy to the dataset by walking forward."""
        dt_column = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN])

        if start_dt is None:
            start_dt = max(
                self._df[[dt_column, x]].dropna()[dt_column].iloc[0].to_pydatetime()
                for x in self._df.attrs[ODDS_COLUMNS_ATTR]
            )

        cols = set(self._df.columns.values)
        training_cols = set(self._df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR])
        x = self._df[list(cols - training_cols)]
        y = self._df[list(training_cols)]
        y[OUTPUT_COLUMN] = np.argmax(y.to_numpy(), axis=1)
        if len(training_cols) == 2:
            y[OUTPUT_COLUMN] = y[OUTPUT_COLUMN].astype(bool)
        y = y[[OUTPUT_COLUMN]]
        x = self._features.process(x)
        x = self._reducers.process(x)

        # Walkforward by week
        predictions = []
        while True:
            start_dt = _next_week_dt(start_dt, x)
            x_walk = x[x[dt_column] < start_dt]
            y_walk = y[y[dt_column] < start_dt]
            if len(x_walk) == len(x) or len(y_walk) == len(y):
                break
            folder = os.path.join(self._name, str(start_dt.date()))
            os.makedirs(folder, exist_ok=True)
            print(f"Trainer {folder}")
            next_dt = _next_week_dt(start_dt, x)
            x_test = x[x[dt_column] >= start_dt]
            x_test = x_test[x_test[dt_column] < next_dt]
            y_test = y[y[dt_column] >= start_dt]
            y_test = y_test[y_test[dt_column] < next_dt]

            def objective(trial: optuna.Trial) -> float:
                trainer = VennAbersTrainer(folder, CatboostTrainer(folder, trial=trial))
                trainer.fit(x_walk, y_walk)
                y_pred = trainer.predict(x_test)
                if y_pred is None:
                    raise ValueError("y_pred is null")
                return accuracy_score(y_test, y_pred[[OUTPUT_COLUMN]])

            self._study.optimize(objective, n_trials=3)
            with open(os.path.join(self._name, _SAMPLER_FILENAME), "wb") as handle:
                pickle.dump(self._study.sampler, handle)
            trainer = VennAbersTrainer(
                folder, CatboostTrainer(folder, trial=self._study.best_trial)
            )
            trainer.fit(x_walk, y_walk)
            trainer.save()

            y_pred = trainer.predict(x_test)
            if y_pred is None:
                raise ValueError("y_pred is null")
            print(y_pred)
            predictions.append(accuracy_score(y_test, y_pred[[OUTPUT_COLUMN]]))
        return statistics.mean(predictions)

    def predict(self, start_dt: datetime.datetime | None = None) -> pd.DataFrame:
        """Predict the results from walk-forward."""
        dt_column = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN])

        if start_dt is None:
            start_dt = max(
                self._df[[dt_column, x]].dropna()[dt_column].iloc[0].to_pydatetime()
                for x in self._df.attrs[ODDS_COLUMNS_ATTR]
            )

        cols = set(self._df.columns.values)
        training_cols = set(self._df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR])
        x = self._df[list(cols - training_cols)]
        x[OUTPUT_COLUMN] = None
        x[OUTPUT_PROB_COLUMN] = None
        while True:
            start_dt = _next_week_dt(start_dt, x)
            x_walk = x[x[dt_column] < start_dt]
            if len(x_walk) == len(x):
                break
            next_dt = _next_week_dt(start_dt, x)
            x_test = x[x[dt_column] >= start_dt]
            x_test = x_test[x_test[dt_column] < next_dt]
            folder = os.path.join(self._name, str(start_dt.date()))
            trainer = VennAbersTrainer(folder, CatboostTrainer(folder))
            trainer.load()
            y_pred = trainer.predict(x_test)
            if y_pred is None:
                raise ValueError("y_pred is null")
            x[OUTPUT_COLUMN] = y_pred[OUTPUT_COLUMN]
            x[OUTPUT_PROB_COLUMN] = y_pred[OUTPUT_PROB_COLUMN]
        return x

    def returns(self) -> pd.Series:
        """Render the returns of the strategy."""
        df = self.predict()
        dt_column = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN])
        training_cols = sorted(list(set(self._df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR])))
        index = []
        data = []
        for date, group in df.groupby([df[dt_column].dt.date]):
            index.append(date)

            # Find the kelly criterion for each bet
            fs = []
            for _, row in group.iterrows():
                team_idx = int(row[OUTPUT_COLUMN])
                prob = row[OUTPUT_PROB_COLUMN]
                odds = self._df.attrs[ODDS_COLUMNS_ATTR][team_idx]
                f = max(prob - ((1.0 - prob) / odds), 0.0)
                fs.append(f)

            # Make sure we aren't overallocating our capital
            fs_sum = sum(fs)
            if fs_sum > 1.0:
                fs = [x / fs_sum for x in fs]

            # Simulate the bets
            bet_idx = 0
            pl = 0.0
            for _, row in group.iterrows():
                team_idx = int(row[OUTPUT_COLUMN])
                win_team_idx = np.argmax(row[training_cols].to_numpy(), axis=1)
                odds = self._df.attrs[ODDS_COLUMNS_ATTR][team_idx]
                if team_idx == win_team_idx:
                    pl += odds * fs[bet_idx]
                else:
                    pl -= fs[bet_idx]
                bet_idx += 1

            data.append(pl)

        return pd.Series(index=index, data=data, name=self._name)
