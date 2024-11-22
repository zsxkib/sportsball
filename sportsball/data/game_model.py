"""The prototype class for a game."""

# pylint: disable=too-many-arguments
import datetime
from typing import Optional, Sequence

import pandas as pd

from .columns import (CATEGORICAL_COLUMNS_ATTR, COLUMN_SEPARATOR,
                      ODDS_COLUMNS_ATTR, POINTS_COLUMNS_ATTR,
                      TEXT_COLUMNS_ATTR, TRAINING_EXCLUDE_COLUMNS_ATTR,
                      update_columns_list)
from .model import Model
from .team_model import TeamModel
from .venue_model import VenueModel

GAME_COLUMN_SUFFIX = "game"
GAME_DT_COLUMN = "dt"
GAME_WEEK_COLUMN = "week"
GAME_END_DT_COLUMN = "end_dt"
GAME_NUMBER_COLUMN = "game_number"
FULL_GAME_DT_COLUMN = COLUMN_SEPARATOR.join([GAME_COLUMN_SUFFIX, GAME_DT_COLUMN])


class GameModel(Model):
    """The prototype game class."""

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        raise NotImplementedError("dt not implemented in parent class.")

    @property
    def week(self) -> int:
        """Return the game week."""
        raise NotImplementedError("week not implemented in parent class.")

    @property
    def game_number(self) -> int:
        """Return the game number."""
        raise NotImplementedError("game_number not implemented in parent class.")

    @property
    def venue(self) -> Optional[VenueModel]:
        """Return the venue the game was played at."""
        return None

    @property
    def teams(self) -> Sequence[TeamModel]:
        """Return the teams within the game."""
        raise NotImplementedError("teams not implemented in parent class.")

    @property
    def home_team(self) -> TeamModel:
        """Return the home team."""
        raise NotImplementedError(
            "home_team not implemented in GameModel parent class."
        )

    @property
    def away_team(self) -> TeamModel:
        """Return the away team."""
        raise NotImplementedError(
            "away_team not implemented in GameModel parent class."
        )

    @property
    def end_dt(self) -> datetime.datetime | None:
        """Return the end time of the game."""
        return None

    def to_frame(self) -> pd.DataFrame:
        """Render the game as a dataframe."""
        # pylint: disable=too-many-locals
        data = {
            GAME_DT_COLUMN: [self.dt],
            GAME_WEEK_COLUMN: [self.week],
            GAME_NUMBER_COLUMN: [self.game_number],
        }

        training_exclude_columns = []
        odds_columns = []
        points_columns = []
        text_columns = []
        categorical_columns = []

        venue = self.venue
        if venue is not None:
            venue_df = venue.to_frame()
            training_exclude_columns.extend(
                venue_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, [])
            )
            odds_columns.extend(venue_df.attrs.get(ODDS_COLUMNS_ATTR, []))
            points_columns.extend(venue_df.attrs.get(POINTS_COLUMNS_ATTR, []))
            text_columns.extend(venue_df.attrs.get(TEXT_COLUMNS_ATTR, []))
            categorical_columns.extend(venue_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, []))
            for column in venue_df.columns.values:
                data[column] = venue_df[column].to_list()

        end_dt = self.end_dt
        if end_dt is not None:
            data[GAME_END_DT_COLUMN] = [end_dt]
            training_exclude_columns.append(GAME_END_DT_COLUMN)

        for count, team in enumerate(self.teams):
            team_df = team.to_frame()
            column_prefix = str(count)
            training_exclude_columns.extend(
                update_columns_list(
                    team_df.attrs.get(TRAINING_EXCLUDE_COLUMNS_ATTR, []), column_prefix
                )
            )
            odds_columns.extend(
                update_columns_list(
                    team_df.attrs.get(ODDS_COLUMNS_ATTR, []), column_prefix
                )
            )
            points_columns.extend(
                update_columns_list(
                    team_df.attrs.get(POINTS_COLUMNS_ATTR, []), column_prefix
                )
            )
            text_columns.extend(
                update_columns_list(
                    team_df.attrs.get(TEXT_COLUMNS_ATTR, []), column_prefix
                )
            )
            categorical_columns.extend(
                update_columns_list(
                    team_df.attrs.get(CATEGORICAL_COLUMNS_ATTR, []), column_prefix
                )
            )
            for column in team_df.columns.values:
                data[COLUMN_SEPARATOR.join([column_prefix, column])] = team_df[
                    column
                ].to_list()

        df = pd.DataFrame(
            data={GAME_COLUMN_SUFFIX + COLUMN_SEPARATOR + k: v for k, v in data.items()}
        )
        df.attrs[TRAINING_EXCLUDE_COLUMNS_ATTR] = list(
            set(update_columns_list(training_exclude_columns, GAME_COLUMN_SUFFIX))
        )
        df.attrs[ODDS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(odds_columns, GAME_COLUMN_SUFFIX)))
        )
        df.attrs[POINTS_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(points_columns, GAME_COLUMN_SUFFIX)))
        )
        df.attrs[TEXT_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(text_columns, GAME_COLUMN_SUFFIX)))
        )
        df.attrs[CATEGORICAL_COLUMNS_ATTR] = sorted(
            list(set(update_columns_list(categorical_columns, GAME_COLUMN_SUFFIX)))
        )
        return df
