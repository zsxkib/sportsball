"""The prototype class for a bookie."""

import pandas as pd

from .columns import COLUMN_SEPARATOR
from .model import Model

BOOKIE_COLUMN_SUFFIX = "bookie"


class BookieModel(Model):
    """The prototype bookie class."""

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        raise ValueError("identifier is not implemented in parent class.")

    @property
    def name(self) -> str:
        """Return the name."""
        raise ValueError("name is not implemented in parent class.")

    def to_frame(self) -> pd.DataFrame:
        """Render the odds as a dataframe."""
        data = {
            "identifier": [self.identifier],
            "name": [self.name],
        }
        return pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([BOOKIE_COLUMN_SUFFIX, k]): v
                for k, v in data.items()
            }
        )
