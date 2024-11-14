"""The prototype class for a venue."""

import pandas as pd

from .address_model import AddressModel
from .columns import (COLUMN_SEPARATOR, ODDS_COLUMNS_ATTR,
                      TRAINING_EXCLUDE_COLUMNS_ATTR, update_columns_list)
from .model import Model

VENUE_COLUMN_SUFFIX = "venue"


class VenueModel(Model):
    """The prototype venue class."""

    @property
    def identifier(self) -> str:
        """Return the venue ID."""
        raise NotImplementedError("identifier is not implemented in parent class.")

    @property
    def name(self) -> str:
        """Return the venue name."""
        raise NotImplementedError("name is not implemented in parent class.")

    @property
    def address(self) -> AddressModel | None:
        """Return the venue address."""
        return None

    def to_frame(self) -> pd.DataFrame:
        """Render the address's dataframe."""
        data = {
            "identifier": [self.identifier],
            "name": [self.name],
        }
        training_exclude_columns = []
        odds_columns = []
        address = self.address
        if address is not None:
            address_df = address.to_frame()
            training_exclude_columns.extend(
                address_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, [])
            )
            odds_columns.extend(address_df.attrs.get(ODDS_COLUMNS_ATTR, []))
            for column in address_df.columns.values:
                data[column] = address_df[column].to_list()
        df = pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([VENUE_COLUMN_SUFFIX, k]): v
                for k, v in data.items()
            }
        )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(update_columns_list(training_exclude_columns, VENUE_COLUMN_SUFFIX))
        )
        df.attrs[ODDS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(odds_columns, VENUE_COLUMN_SUFFIX)))
        )
        return df
