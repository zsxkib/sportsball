"""The prototype class for a game."""

# pylint: disable=too-many-arguments
import datetime
from typing import Optional, Sequence

import pandas as pd
import requests_cache

from .team_model import TeamModel
from .venue_model import VenueModel

GAME_COLUMN_SUFFIX = "game_"
GAME_DT_COLUMN = "dt"


class GameModel:
    """The prototype game class."""

    def __init__(
        self,
        dt: datetime.datetime,
        week: int,
        game_number: int,
        venue: Optional[VenueModel],
        teams: Sequence[TeamModel],
        session: requests_cache.CachedSession,
    ) -> None:
        self._dt = dt
        self._week = week
        self._game_number = game_number
        self._venue_model = venue
        self._teams = teams
        self._session = session

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        return self._dt

    @property
    def week(self) -> int:
        """Return the game week."""
        return self._week

    @property
    def game_number(self) -> int:
        """Return the game number."""
        return self._game_number

    @property
    def venue(self) -> Optional[VenueModel]:
        """Return the venue the game was played at."""
        return self._venue_model

    @property
    def teams(self) -> Sequence[TeamModel]:
        """Return the teams within the game."""
        return self._teams

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
    def session(self) -> requests_cache.CachedSession:
        """Return the cached session."""
        return self._session

    @property
    def end_dt(self) -> datetime.datetime:
        """Return the end time of the game."""
        # Figure out a way to get this without averages.
        return self.dt + datetime.timedelta(hours=3, minutes=12)

    def to_frame(self) -> pd.DataFrame:
        """Render the game as a dataframe."""
        data = {
            GAME_DT_COLUMN: [self.dt],
            "week": [self.week],
            "game_number": [self.game_number],
            "end_dt": [self.end_dt],
        }

        if self.venue is not None:
            venue_df = self.venue.to_frame()
            for column in venue_df.columns.values:
                data[column] = venue_df[column].to_list()

        for count, team in enumerate(self.teams):
            team_df = team.to_frame()
            for column in team_df.columns.values:
                data[str(count) + "_" + column] = team_df[column].to_list()

        return pd.DataFrame(data={GAME_COLUMN_SUFFIX + k: v for k, v in data.items()})
