"""The total feature extractor."""

import pandas as pd

from ...data.columns import COLUMN_SEPARATOR
from ...data.venue_model import VENUE_COLUMN_PREFIX
from .columns import (find_player_count, find_team_count, player_column_prefix,
                      player_identifier_column, team_column_prefix,
                      team_identifier_column, venue_identifier_column)
from .feature import Feature

TOTAL_COLUMN_PREFIX = "total"
TOTAL_GAMES_COLUMN = "games"


def _process_player_team_games(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    team_count = find_team_count(df)
    player_count = find_player_count(df, team_count)
    player_team_games: dict[str, int] = {}
    for i in range(team_count):
        for j in range(player_count):
            total_attendance_col = COLUMN_SEPARATOR.join(
                [TOTAL_COLUMN_PREFIX, player_column_prefix(i, j), TOTAL_GAMES_COLUMN]
            )
            df[total_attendance_col] = None
    for row in df[cols].itertuples():
        for i in range(team_count):
            team_idx = row[cols.index(team_identifier_column(i)) + 1]
            for j in range(player_count):
                player_idx = row[cols.index(player_identifier_column(i, j)) + 1]
                key = "-".join([team_idx, player_idx])
                count = player_team_games.get(key, 0)
                total_attendance_col = COLUMN_SEPARATOR.join(
                    [
                        TOTAL_COLUMN_PREFIX,
                        player_column_prefix(i, j),
                        TOTAL_GAMES_COLUMN,
                    ]
                )
                df.loc[row.Index, total_attendance_col] = count
                player_team_games[key] = count + 1
    return df


def _process_team_venue_games(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    venue_col = venue_identifier_column()
    if venue_col not in cols:
        return df
    team_count = find_team_count(df)
    for i in range(team_count):
        total_venue_col = COLUMN_SEPARATOR.join(
            [
                TOTAL_COLUMN_PREFIX,
                team_column_prefix(i),
                VENUE_COLUMN_PREFIX,
                TOTAL_GAMES_COLUMN,
            ]
        )
        df[total_venue_col] = None
    venue_team_games: dict[str, int] = {}
    for row in df[cols].itertuples():
        for i in range(team_count):
            team_idx = row[cols.index(team_identifier_column(i)) + 1]
            venue_idx = row[cols.index(venue_identifier_column()) + 1]
            key = "-".join([team_idx, venue_idx])
            count = venue_team_games.get(key, 0)
            total_venue_col = COLUMN_SEPARATOR.join(
                [
                    TOTAL_COLUMN_PREFIX,
                    team_column_prefix(i),
                    VENUE_COLUMN_PREFIX,
                    TOTAL_GAMES_COLUMN,
                ]
            )
            df.loc[row.Index, total_venue_col] = count
            venue_team_games[key] = count + 1
    return df


class TotalFeature(Feature):
    """The total feature extractor class."""

    # pylint: disable=too-few-public-methods

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the dataframe and add the necessary features."""
        cols = df.columns.values.tolist()
        df = _process_player_team_games(df, cols)
        df = _process_team_venue_games(df, cols)
        return df.copy()
