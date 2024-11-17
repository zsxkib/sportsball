"""The prototype class for a player."""

from typing import Optional

import pandas as pd

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      update_columns_list)
from .model import Model

PLAYER_COLUMN_SUFFIX = "player"
IDENTIFIER_COLUMN = "identifier"
JERSEY_COLUMN = "jersey"


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

    def to_frame(self) -> pd.DataFrame:
        """Render the player as a dataframe."""
        data = {
            IDENTIFIER_COLUMN: [self.identifier],
            JERSEY_COLUMN: [self.jersey],
        }

        df = pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([PLAYER_COLUMN_SUFFIX, k]): v
                for k, v in data.items()
            }
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = list(
            set(
                update_columns_list(
                    [IDENTIFIER_COLUMN, JERSEY_COLUMN], PLAYER_COLUMN_SUFFIX
                )
            )
        )
        return df
