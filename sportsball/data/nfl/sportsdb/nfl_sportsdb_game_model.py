"""NFL SportsDB game model."""
# pylint: disable=duplicate-code

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import pytz
import requests
from dateutil import parser

from ...game_model import GameModel
from ...team_model import TeamModel
from ...venue_model import VenueModel
from .nfl_sportsdb_team_model import NFLSportsDBTablesTeamModel
from .nfl_sportsdb_venue_model import NFLSportsDBVenueModel


class NFLSportsDBGameModel(GameModel):
    """NFL SportsDB implementation of the game model."""

    _teams: Sequence[TeamModel] | None
    _venue_model: VenueModel | None

    def __init__(
        self,
        session: requests.Session,
        game: dict[str, Any],
        week: int,
        game_number: int,
    ) -> None:
        super().__init__(session)
        self._game = game
        try:
            self._dt = datetime.datetime.fromisoformat(game["strTimestamp"])
        except TypeError:
            self._dt = parser.parse(game["dateEvent"])
        self._sportsdb_week = week
        self._game_number = game_number
        self._teams = None
        self._venue_model = None

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        dt = self._dt
        tz = None
        venue_model = self.venue
        if venue_model is not None:
            address = venue_model.address
            if address is not None:
                timezone = address.timezone
                if timezone is not None:
                    tz = pytz.timezone(timezone)
        if tz is None:
            tz = pytz.utc
        return tz.localize(dt)

    @property
    def week(self) -> int:
        """Return the game week."""
        return self._sportsdb_week

    @property
    def game_number(self) -> int:
        """Return the game number."""
        return self._game_number

    @property
    def home_team(self) -> TeamModel:
        return self.teams[0]

    @property
    def away_team(self) -> TeamModel:
        return self.teams[1]

    @property
    def venue(self) -> Optional[VenueModel]:
        venue = self._venue_model
        if venue is None:
            try:
                venue = NFLSportsDBVenueModel(
                    self.session, self._dt, self._game["idVenue"]
                )
            except TypeError:
                pass
            self._venue_model = venue
        return venue

    @property
    def teams(self) -> Sequence[TeamModel]:
        teams = self._teams
        if teams is None:
            home_score = float(
                self._game["intHomeScore"]
                if self._game["intHomeScore"] is not None
                else 0
            )
            away_score = float(
                self._game["intAwayScore"]
                if self._game["intAwayScore"] is not None
                else 0
            )
            teams = [
                NFLSportsDBTablesTeamModel(
                    self.session,
                    self._game["idHomeTeam"],
                    self._game["strHomeTeam"],
                    home_score,
                ),
                NFLSportsDBTablesTeamModel(
                    self.session,
                    self._game["idAwayTeam"],
                    self._game["strAwayTeam"],
                    away_score,
                ),
            ]
            self._teams = teams
        return teams

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **NFLSportsDBVenueModel.urls_expire_after(),
            **NFLSportsDBTablesTeamModel.urls_expire_after(),
        }
