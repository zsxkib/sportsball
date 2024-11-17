"""The prototype class for a bookie."""

import pandas as pd

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR,
                      update_columns_list)
from .model import Model

BOOKIE_COLUMN_SUFFIX = "bookie"
IDENTIFIER_COLUMN = "identifier"
NAME_COLUMN = "name"


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
            IDENTIFIER_COLUMN: [self.identifier],
            NAME_COLUMN: [self.name],
        }
        df = pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([BOOKIE_COLUMN_SUFFIX, k]): v
                for k, v in data.items()
            }
        )
        df.attrs[TEXT_COLUMNS_ATTR] = list(
            set(update_columns_list([NAME_COLUMN], BOOKIE_COLUMN_SUFFIX))
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = list(
            set(update_columns_list([IDENTIFIER_COLUMN], BOOKIE_COLUMN_SUFFIX))
        )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(update_columns_list([NAME_COLUMN], BOOKIE_COLUMN_SUFFIX))
        )
        return df
