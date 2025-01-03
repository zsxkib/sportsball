"""Helper functions for columns."""

import pandas as pd

from ...data.game_model import (GAME_ATTENDANCE_COLUMN, TEAM_COLUMN_PREFIX,
                                VENUE_COLUMN_PREFIX)
from ...data.league_model import DELIMITER
from ...data.player_model import PLAYER_IDENTIFIER_COLUMN, PLAYER_KICKS_COLUMN
from ...data.team_model import (PLAYER_COLUMN_PREFIX, TEAM_IDENTIFIER_COLUMN,
                                TEAM_POINTS_COLUMN)
from ...data.venue_model import VENUE_IDENTIFIER_COLUMN


def team_column_prefix(team_idx: int) -> str:
    """Generate a prefix for a team column at a given index."""
    return DELIMITER.join(
        [
            TEAM_COLUMN_PREFIX,
            str(team_idx),
        ]
    )


def team_identifier_column(team_idx: int) -> str:
    """Generate a team identifier column at a given index."""
    return DELIMITER.join([team_column_prefix(team_idx), TEAM_IDENTIFIER_COLUMN])


def team_points_column(team_idx: int) -> str:
    """Generate a team points column at a given index."""
    return DELIMITER.join([team_column_prefix(team_idx), TEAM_POINTS_COLUMN])


def player_column_prefix(team_idx: int, player_idx: int | None) -> str:
    """Generate a prefix for a player column at a given index."""
    if player_idx is None:
        return DELIMITER.join(
            [
                team_column_prefix(team_idx),
                PLAYER_COLUMN_PREFIX,
            ]
        )
    return DELIMITER.join(
        [
            team_column_prefix(team_idx),
            PLAYER_COLUMN_PREFIX,
            str(player_idx),
        ]
    )


def player_identifier_column(team_idx: int, player_idx: int) -> str:
    """Generate a team points column at a given index."""
    return DELIMITER.join(
        [player_column_prefix(team_idx, player_idx), PLAYER_IDENTIFIER_COLUMN]
    )


def attendance_column() -> str:
    """Generate an attendance column."""
    return DELIMITER.join([GAME_ATTENDANCE_COLUMN])


def find_team_count(df: pd.DataFrame) -> int:
    """Find the number of teams in the dataframe."""
    team_count = 0
    while True:
        if team_identifier_column(team_count) not in df.columns.values:
            break
        team_count += 1
    return team_count


def find_player_count(df: pd.DataFrame, team_count: int) -> int:
    """Find the number of players in a team in the dataframe."""
    player_count = 0
    while True:
        found_player = False
        for i in range(team_count):
            if player_identifier_column(i, player_count) not in df.columns.values:
                continue
            found_player = True
        if not found_player:
            break
        player_count += 1
    return player_count


def venue_identifier_column() -> str:
    """Generate a venue identifier column."""
    return DELIMITER.join([VENUE_COLUMN_PREFIX, VENUE_IDENTIFIER_COLUMN])


def kick_column(team_idx: int, player_idx: int) -> str:
    """Generate a kick column."""
    return DELIMITER.join(
        [player_column_prefix(team_idx, player_idx), PLAYER_KICKS_COLUMN]
    )
