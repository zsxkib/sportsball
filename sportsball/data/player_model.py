"""The prototype class for a player."""

from typing import Optional

import pandas as pd

from .columns import COLUMN_SEPARATOR
from .model import Model

PLAYER_COLUMN_SUFFIX = "player"


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
            "identifier": [self.identifier],
            "jersey": [self.jersey],
        }

        return pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([PLAYER_COLUMN_SUFFIX, k]): v
                for k, v in data.items()
            }
        )
