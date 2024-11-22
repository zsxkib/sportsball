"""The prototype class for a team."""

# pylint: disable=too-many-arguments
from typing import Sequence

import pandas as pd

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      ODDS_COLUMNS_ATTR, POINTS_COLUMNS_ATTR,
                      TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR,
                      update_columns_list)
from .model import Model
from .odds_model import OddsModel
from .player_model import PlayerModel

TEAM_COLUMN_SUFFIX = "team"
POINTS_COLUMN = "points"
TEAM_IDENTIFIER_COLUMN = "identifier"
NAME_COLUMN = "name"
LOCATION_COLUMN = "location"


class TeamModel(Model):
    """The prototype team class."""

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        raise NotImplementedError("identifier is not implemented in parent class.")

    @property
    def name(self) -> str:
        """Return the name."""
        raise NotImplementedError("name is not implemented in parent class.")

    @property
    def location(self) -> str | None:
        """Return the location."""
        return None

    @property
    def players(self) -> Sequence[PlayerModel]:
        """Return a list of players in the team."""
        raise NotImplementedError("players is not implemented in parent class.")

    @property
    def odds(self) -> Sequence[OddsModel]:
        """Return the odds."""
        return []

    @property
    def points(self) -> float | None:
        """Return the points scored in the game."""
        return None

    def to_frame(self) -> pd.DataFrame:
        """Render the team as a dataframe."""
        # pylint: disable=too-many-locals
        data: dict[str, list[str | float]] = {
            TEAM_IDENTIFIER_COLUMN: [self.identifier],
            NAME_COLUMN: [self.name],
        }

        training_exclude_columns = [NAME_COLUMN]
        odds_columns = []
        points_columns = []
        text_columns = [NAME_COLUMN]
        categorical_columns = [TEAM_IDENTIFIER_COLUMN]

        for count, player in enumerate(self.players):
            player_df = player.to_frame()
            column_prefix = str(count)
            training_exclude_columns.extend(
                update_columns_list(
                    player_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, []),
                    column_prefix,
                )
            )
            odds_columns.extend(
                update_columns_list(
                    player_df.attrs.get(ODDS_COLUMNS_ATTR, []), column_prefix
                )
            )
            points_columns.extend(
                update_columns_list(
                    player_df.attrs.get(POINTS_COLUMNS_ATTR, []), column_prefix
                )
            )
            text_columns.extend(
                update_columns_list(
                    player_df.attrs.get(TEXT_COLUMNS_ATTR, []), column_prefix
                )
            )
            categorical_columns.extend(
                update_columns_list(
                    player_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, []), column_prefix
                )
            )
            for column in player_df.columns.values:
                data[COLUMN_SEPARATOR.join([column_prefix, column])] = player_df[
                    column
                ].to_list()

        for count, odds in enumerate(
            sorted(self.odds, key=lambda x: x.bookie.identifier)
        ):
            odds_df = odds.to_frame()
            column_prefix = str(count)
            training_exclude_columns.extend(
                update_columns_list(
                    odds_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, []), column_prefix
                )
            )
            odds_columns.extend(
                update_columns_list(
                    odds_df.attrs.get(ODDS_COLUMNS_ATTR, []), column_prefix
                )
            )
            points_columns.extend(
                update_columns_list(
                    odds_df.attrs.get(POINTS_COLUMNS_ATTR, []), column_prefix
                )
            )
            text_columns.extend(
                update_columns_list(
                    odds_df.attrs.get(TEXT_COLUMNS_ATTR, []), column_prefix
                )
            )
            categorical_columns.extend(
                update_columns_list(
                    odds_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, []), column_prefix
                )
            )
            for column in odds_df.columns.values:
                data[COLUMN_SEPARATOR.join([column_prefix, column])] = odds_df[
                    column
                ].to_list()

        points = self.points
        if points is not None:
            data[POINTS_COLUMN] = [points]
            training_exclude_columns.append(POINTS_COLUMN)
            points_columns.append(POINTS_COLUMN)

        location = self.location
        if location is not None:
            data[LOCATION_COLUMN] = [location]
            categorical_columns.append(LOCATION_COLUMN)

        df = pd.DataFrame(
            data={TEAM_COLUMN_SUFFIX + COLUMN_SEPARATOR + k: v for k, v in data.items()}
        )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(update_columns_list(training_exclude_columns, TEAM_COLUMN_SUFFIX))
        )
        df.attrs[ODDS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(odds_columns, TEAM_COLUMN_SUFFIX)))
        )
        df.attrs[POINTS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(points_columns, TEAM_COLUMN_SUFFIX)))
        )
        df.attrs[TEXT_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(text_columns, TEAM_COLUMN_SUFFIX)))
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(categorical_columns, TEAM_COLUMN_SUFFIX)))
        )
        return df
