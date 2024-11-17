"""Some constants and functions for determining columns for training."""

TRAINING_EXCLUDE_COLUMNS_ATTR = "training_exclude"
ODDS_COLUMNS_ATTR = "odds"
POINTS_COLUMNS_ATTR = "points"
CATEGORICAL_COLUMNS_ATTR = "categorical"
TEXT_COLUMNS_ATTR = "text"
COLUMN_SEPARATOR = "_"


def update_columns_list(columns: list[str], column_prefix: str) -> list[str]:
    """Updates training exclusion columns for a new column prefix."""
    return [COLUMN_SEPARATOR.join([column_prefix, x]) for x in columns]
