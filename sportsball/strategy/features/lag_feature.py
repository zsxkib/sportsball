"""The lag feature extractor."""

import pandas as pd

from ...data.columns import COLUMN_SEPARATOR
from .columns import (attendance_column, find_player_count, find_team_count,
                      kick_column, player_identifier_column,
                      team_identifier_column, venue_identifier_column)
from .feature import Feature

LAG_COLUMN_PREFIX = "lag"


def _process_attendance(df: pd.DataFrame) -> pd.DataFrame:
    attendance_col = attendance_column()
    if attendance_col in df.columns.values:
        team_count = find_team_count(df)
        lag_attendance_col = COLUMN_SEPARATOR.join([LAG_COLUMN_PREFIX, attendance_col])
        df[lag_attendance_col] = None
        last_attendances: dict[str, int | None] = {}

        def record_lagged_attendence(row: pd.Series) -> pd.Series:
            nonlocal team_count
            attendance_key_components = [row[venue_identifier_column()]]
            for i in range(team_count):
                attendance_key_components.append(row[team_identifier_column(i)])
            attendance_key = "-".join(attendance_key_components)
            row[lag_attendance_col] = last_attendances.get(attendance_key)
            last_attendances[attendance_key] = row[attendance_col]
            return row

        df = df.apply(record_lagged_attendence, axis=1)

    return df


def _process_kicks(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    team_count = find_team_count(df)
    player_count = find_player_count(df, team_count)
    last_kicks: dict[str, int | None] = {}
    for row in df.itertuples():
        for i in range(team_count):
            for j in range(player_count):
                kick_col = kick_column(i, j)
                if kick_col not in cols:
                    continue
                lag_kick_col = COLUMN_SEPARATOR.join([LAG_COLUMN_PREFIX, kick_col])
                player_idx = row[cols.index(player_identifier_column(i, j)) + 1]
                df.loc[row.Index, lag_kick_col] = last_kicks.get(player_idx)
                last_kicks[player_idx] = row[cols.index(kick_col) + 1]
    return df


class LagFeature(Feature):
    """The lag feature extractor class."""

    # pylint: disable=too-few-public-methods

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the dataframe and add the necessary features."""
        cols = df.columns.values.tolist()
        df = _process_attendance(df)
        df = _process_kicks(df, cols)
        return df.copy()
