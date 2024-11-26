"""Helper functions for columns."""

from ...data.columns import COLUMN_SEPARATOR
from ...data.game_model import GAME_COLUMN_SUFFIX
from ...data.player_model import PLAYER_COLUMN_SUFFIX, PLAYER_IDENTIFIER_COLUMN
from ...data.team_model import (TEAM_COLUMN_SUFFIX, TEAM_IDENTIFIER_COLUMN,
                                TEAM_POINTS_COLUMN)


def team_column_prefix(team_idx: int) -> str:
    """Generate a prefix for a team column at a given index."""
    return COLUMN_SEPARATOR.join(
        [
            GAME_COLUMN_SUFFIX,
            str(team_idx),
            TEAM_COLUMN_SUFFIX,
        ]
    )


def team_identifier_column(team_idx: int) -> str:
    """Generate a team identifier column at a given index."""
    return COLUMN_SEPARATOR.join([team_column_prefix(team_idx), TEAM_IDENTIFIER_COLUMN])


def team_points_column(team_idx: int) -> str:
    """Generate a team points column at a given index."""
    return COLUMN_SEPARATOR.join([team_column_prefix(team_idx), TEAM_POINTS_COLUMN])


def player_column_prefix(team_idx: int, player_idx: int) -> str:
    """Generate a prefix for a player column at a given index."""
    return COLUMN_SEPARATOR.join(
        [
            team_column_prefix(team_idx),
            str(player_idx),
            PLAYER_COLUMN_SUFFIX,
        ]
    )


def player_identifier_column(team_idx: int, player_idx: int) -> str:
    """Generate a team points column at a given index."""
    return COLUMN_SEPARATOR.join(
        [player_column_prefix(team_idx, player_idx), PLAYER_IDENTIFIER_COLUMN]
    )
