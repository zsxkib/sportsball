"""The prototype class for a player."""

from typing import Optional

import pandas as pd

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      TRAINING_EXCLUDE_COLUMNS_ATTR, update_columns_list)
from .model import Model

PLAYER_COLUMN_PREFIX = "player"
PLAYER_IDENTIFIER_COLUMN = "identifier"
JERSEY_COLUMN = "jersey"
PLAYER_KICKS_COLUMN = "kicks"


class PlayerModel(Model):
    """The prototype player class."""

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        raise NotImplementedError("identifier not implemented in parent class.")

    @property
    def jersey(self) -> Optional[str]:
        """Return the jersey."""
        raise NotImplementedError("jersey not implemented in parent class.")

    @property
    def kicks(self) -> int | None:
        """Return the number of kicks for this player in a game."""
        return None

    def to_frame(self) -> pd.DataFrame:
        """Render the player as a dataframe."""
        data = {
            PLAYER_IDENTIFIER_COLUMN: [self.identifier],
            JERSEY_COLUMN: [self.jersey],
        }

        training_exclude_columns = []
        kicks = self.kicks
        if kicks is not None:
            data[PLAYER_KICKS_COLUMN] = [kicks]
            training_exclude_columns.append(PLAYER_KICKS_COLUMN)

        df = pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([PLAYER_COLUMN_PREFIX, k]): v
                for k, v in data.items()
            }
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = list(
            set(
                update_columns_list(
                    [PLAYER_IDENTIFIER_COLUMN, JERSEY_COLUMN], PLAYER_COLUMN_PREFIX
                )
            )
        )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(update_columns_list(training_exclude_columns, PLAYER_COLUMN_PREFIX))
        )
        return df
