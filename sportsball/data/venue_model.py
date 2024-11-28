"""The prototype class for a venue."""

import pandas as pd

from .address_model import AddressModel
from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      ODDS_COLUMNS_ATTR, POINTS_COLUMNS_ATTR,
                      TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR,
                      update_columns_list)
from .model import Model

VENUE_COLUMN_PREFIX = "venue"
VENUE_IDENTIFIER_COLUMN = "identifier"
NAME_COLUMN = "name"


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
        # pylint: disable=duplicate-code
        data = {
            VENUE_IDENTIFIER_COLUMN: [self.identifier],
            NAME_COLUMN: [self.name],
        }

        training_exclude_columns = [NAME_COLUMN]
        odds_columns = []
        points_columns = []
        text_columns = [NAME_COLUMN]
        categorical_columns = [VENUE_IDENTIFIER_COLUMN]

        address = self.address
        if address is not None:
            address_df = address.to_frame()
            training_exclude_columns.extend(
                address_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, [])
            )
            odds_columns.extend(address_df.attrs.get(ODDS_COLUMNS_ATTR, []))
            points_columns.extend(address_df.attrs.get(POINTS_COLUMNS_ATTR, []))
            text_columns.extend(address_df.attrs.get(TEXT_COLUMNS_ATTR, []))
            categorical_columns.extend(
                address_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, [])
            )
            for column in address_df.columns.values:
                data[column] = address_df[column].to_list()
        df = pd.DataFrame(
            data={
                COLUMN_SEPARATOR.join([VENUE_COLUMN_PREFIX, k]): v
                for k, v in data.items()
            }
        )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(update_columns_list(training_exclude_columns, VENUE_COLUMN_PREFIX))
        )
        df.attrs[ODDS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(odds_columns, VENUE_COLUMN_PREFIX)))
        )
        df.attrs[POINTS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(points_columns, VENUE_COLUMN_PREFIX)))
        )
        df.attrs[TEXT_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(points_columns, VENUE_COLUMN_PREFIX)))
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(points_columns, VENUE_COLUMN_PREFIX)))
        )
        return df
