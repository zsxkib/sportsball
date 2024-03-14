"""The prototype class for a player."""

from typing import Optional

import pandas as pd


class PlayerModel:
    """The prototype player class."""

    def __init__(self, identifier: str, jersey: Optional[str]) -> None:
        self._identifier = identifier
        self._jersey = jersey

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def jersey(self) -> Optional[str]:
        """Return the jersey."""
        return self._jersey

    def to_frame(self) -> pd.DataFrame:
        """Render the player as a dataframe."""
        data = {
            "identifier": [self.identifier],
            "jersey": [self.jersey],
        }

        return pd.DataFrame(data={"player_" + k: v for k, v in data.items()})
