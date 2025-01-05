"""The lag feature extractor."""

import pandas as pd

from ...data.league_model import DELIMITER
from .columns import (attendance_column, find_player_count, find_team_count,
                      kick_column, player_identifier_column,
                      team_identifier_column, venue_identifier_column)
from .feature import Feature

LAG_COLUMN_PREFIX = "lag"


def _process_attendance(df: pd.DataFrame) -> pd.DataFrame:
    attendance_col = attendance_column()
    if attendance_col in df.columns.values:
        team_count = find_team_count(df)
        lag_attendance_col = DELIMITER.join([LAG_COLUMN_PREFIX, attendance_col])
        df[lag_attendance_col] = None
        last_attendances: dict[str, int | None] = {}

        def record_lagged_attendence(row: pd.Series) -> pd.Series:
            nonlocal team_count
            nonlocal last_attendances
            venue_idx_col = venue_identifier_column()
            try:
                venue_idx = str(row[venue_idx_col])
            except KeyError:
                return row
            attendance_key_components = [venue_idx]
            for i in range(team_count):
                attendance_key_components.append(row[team_identifier_column(i)])
            attendance_key = "-".join(attendance_key_components)
            row[lag_attendance_col] = last_attendances.get(attendance_key)
            last_attendances[attendance_key] = row[attendance_col]
            return row

        df = df.apply(record_lagged_attendence, axis=1)

    return df


def _process_kicks(df: pd.DataFrame) -> pd.DataFrame:
    team_count = find_team_count(df)
    player_count = find_player_count(df, team_count)
    last_kicks: dict[str, int | None] = {}
    for i in range(team_count):
        for j in range(player_count):
            kick_col = kick_column(i, j)
            lag_kick_col = DELIMITER.join([LAG_COLUMN_PREFIX, kick_col])
            df[lag_kick_col] = None

    def record_team_player_kicks(row: pd.Series) -> pd.Series:
        nonlocal team_count
        nonlocal player_count
        nonlocal last_kicks
        for i in range(team_count):
            for j in range(player_count):
                kick_col = kick_column(i, j)
                lag_kick_col = DELIMITER.join([LAG_COLUMN_PREFIX, kick_col])
                player_idx = None
                try:
                    player_idx = row[player_identifier_column(i, j)]
                except KeyError:
                    continue
                row[lag_kick_col] = last_kicks.get(player_idx)
                try:
                    last_kicks[player_idx] = row[kick_col]
                except KeyError:
                    last_kicks[player_idx] = None
        return row

    return df.apply(record_team_player_kicks, axis=1)


class LagFeature(Feature):
    """The lag feature extractor class."""

    # pylint: disable=too-few-public-methods

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the dataframe and add the necessary features."""
        df = _process_attendance(df)
        df = _process_kicks(df)
        return df.copy()
