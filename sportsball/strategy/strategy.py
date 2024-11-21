"""The strategy class."""

import datetime
import os
import pickle
import statistics
import uuid

import numpy as np
import optuna
import pandas as pd
from sklearn.metrics import precision_score  # type: ignore
from sklearn.metrics import accuracy_score, recall_score

from ..data.columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                            ODDS_COLUMNS_ATTR, POINTS_COLUMNS_ATTR,
                            TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR)
from ..data.game_model import (GAME_COLUMN_SUFFIX, GAME_DT_COLUMN,
                               GAME_WEEK_COLUMN)
from .features import CombinedFeature
from .reducers import CombinedReducer
from .trainers import HASH_USR_ATTR, CatboostTrainer, VennAbersTrainer
from .trainers.output_column import OUTPUT_COLUMN

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
            return pd.to_datetime(row[dt_column]).to_pydatetime()
    return pd.to_datetime(df[dt_column]).to_pydatetime()[-1]  # type: ignore


def _print_metrics(y_test: pd.DataFrame, y_pred: pd.DataFrame) -> float:
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision_score(y_test, y_pred)}")
    print(f"Recall: {recall_score(y_test, y_pred)}")
    return accuracy


class Strategy:
    """The strategy class."""

    # pylint: disable=too-many-locals

    def __init__(self, df: pd.DataFrame, name: str) -> None:
        self._df = df
        self._name = name
        self._features = CombinedFeature()
        self._reducers = CombinedReducer(
            [
                COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_WEEK_COLUMN]),
                COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN]),
            ]
        )
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
            direction=optuna.study.StudyDirection.MAXIMIZE,
        )

    def fit(self, start_dt: datetime.datetime | None = None):
        """Fits the strategy to the dataset by walking forward."""
        # pylint: disable=too-many-statements
        dt_column = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN])

        if start_dt is None:
            start_dt = max(
                self._df[[dt_column, x]].dropna()[dt_column].iloc[0].to_pydatetime()
                for x in self._df.attrs[ODDS_COLUMNS_ATTR]
            )

        cols = set(self._df.columns.values)
        training_cols = set(self._df.attrs[POINTS_COLUMNS_ATTR])
        x = self._df[list(cols - set(self._df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR]))]
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
            y_walk = y.iloc[: len(x_walk)]
            if len(x_walk) == len(x) or len(y_walk) == len(y):
                break
            folder = os.path.join(self._name, str(start_dt.date()))
            os.makedirs(folder, exist_ok=True)
            print(f"Trainer {folder}")
            # next_dt = _next_week_dt(start_dt, x)
            x_test = x[x[dt_column] >= start_dt]
            y_test = y.iloc[len(x_walk) : len(x_walk) + len(x_test)]

            def objective(trial: optuna.Trial) -> float:
                trial.set_user_attr(HASH_USR_ATTR, str(uuid.uuid4()))
                trainer = VennAbersTrainer(
                    folder,
                    CatboostTrainer(
                        folder,
                        self._df.attrs[CATEGORICAL_COLUMNS_ATTR],
                        self._df.attrs[TEXT_COLUMNS_ATTR],
                        trial=trial,
                    ),
                )
                features = trainer.select_features(x_walk, y_walk)
                trial.set_user_attr("FEATURES", features)
                trainer.fit(x_walk[features], y_walk)

                y_pred = trainer.predict(x_walk)
                if y_pred is None:
                    raise ValueError("y_pred is null")

                print("In Sample Metrics:")
                _print_metrics(y_walk, y_pred)

                y_pred = trainer.predict(x_test)
                if y_pred is None:
                    raise ValueError("y_pred is null")

                print("Out of Sample Metrics:")
                return _print_metrics(y_test, y_pred)

            self._study.optimize(objective, n_trials=3)
            with open(os.path.join(self._name, _SAMPLER_FILENAME), "wb") as handle:
                pickle.dump(self._study.sampler, handle)
            best_trial = self._study.best_trial
            trainer = VennAbersTrainer(
                folder,
                CatboostTrainer(
                    folder,
                    self._df.attrs[CATEGORICAL_COLUMNS_ATTR],
                    self._df.attrs[TEXT_COLUMNS_ATTR],
                    trial=best_trial,
                ),
            )
            trainer.fit(x_walk[best_trial.user_attrs["FEATURES"]], y_walk)
            trainer.save()

            y_pred = trainer.predict(x_walk)
            if y_pred is None:
                raise ValueError("y_pred is null")
            print("Final In Sample Metrics:")
            _print_metrics(y_walk, y_pred)

            y_pred = trainer.predict(x_test)
            if y_pred is None:
                raise ValueError("y_pred is null")

            print("Final Out of Sample Metrics:")
            predictions.append(_print_metrics(y_test, y_pred))
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
        while True:
            start_dt = _next_week_dt(start_dt, x)
            x_walk = x[x[dt_column] < start_dt]
            if len(x_walk) == len(x):
                break
            next_dt = _next_week_dt(start_dt, x)
            x_test = x[x[dt_column] >= start_dt]
            x_test = x_test[x_test[dt_column] < next_dt]
            folder = os.path.join(self._name, str(start_dt.date()))
            trainer = VennAbersTrainer(
                folder,
                CatboostTrainer(
                    folder,
                    self._df.attrs[CATEGORICAL_COLUMNS_ATTR],
                    self._df.attrs[TEXT_COLUMNS_ATTR],
                ),
            )
            trainer.load()
            y_prob = trainer.predict_proba(x_test)
            if y_prob is None:
                raise ValueError("y_prob is null")

            for column in y_prob.columns.values:
                if column not in x:
                    x[column] = None
                x[column] = y_prob[column]
        return x

    def returns(self) -> pd.Series:
        """Render the returns of the strategy."""
        df = self.predict()
        dt_column = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN])
        points_cols = sorted(list(set(self._df.attrs[POINTS_COLUMNS_ATTR])))
        index = []
        data = []
        for date, group in df.groupby([df[dt_column].dt.date]):
            index.append(date)

            # Find the kelly criterion for each bet
            fs = []
            for _, row in group.iterrows():
                arr = row.to_numpy()
                team_idx = np.argmax(arr)
                prob = arr[team_idx]
                odds = 1.0 / self._df.attrs[ODDS_COLUMNS_ATTR][team_idx]
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
                arr = row.to_numpy()
                team_idx = np.argmax(arr)
                win_team_idx = np.argmax(row[points_cols].to_numpy(), axis=1)
                odds = self._df.attrs[ODDS_COLUMNS_ATTR][team_idx]
                if team_idx == win_team_idx:
                    pl += odds * fs[bet_idx]
                else:
                    pl -= fs[bet_idx]
                bet_idx += 1

            data.append(pl)

        return pd.Series(index=index, data=data, name=self._name)
