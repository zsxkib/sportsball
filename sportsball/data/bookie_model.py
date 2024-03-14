"""The prototype class for a bookie."""

import pandas as pd


class BookieModel:
    """The prototype bookie class."""

    def __init__(self, identifier: str, name: str) -> None:
        self._identifier = identifier
        self._name = name

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    def to_frame(self) -> pd.DataFrame:
        """Render the odds as a dataframe."""
        data = {
            "identifier": [self.identifier],
            "name": [self.name],
        }
        return pd.DataFrame(data={"bookie_" + k: v for k, v in data.items()})
