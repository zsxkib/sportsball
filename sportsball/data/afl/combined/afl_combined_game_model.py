"""AFL combined game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import requests_cache

from ...game_model import GameModel
from ...team_model import TeamModel
from ...venue_model import VenueModel
from ..afltables.afl_afltables_game_model import AFLAFLTablesGameModel
from .afl_combined_team_model import AFLCombinedTeamModel
from .afl_combined_venue_model import AFLCombinedVenueModel


class AFLCombinedGameModel(GameModel):
    """AFL combined implementation of the game model."""

    def __init__(
        self, session: requests_cache.CachedSession, game_model: GameModel
    ) -> None:
        super().__init__(session)
        self._game_model = game_model

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        return self._game_model.dt

    @property
    def week(self) -> int:
        """Return the game week."""
        return self._game_model.week

    @property
    def game_number(self) -> int:
        """Return the game number."""
        return self._game_model.game_number

    @property
    def home_team(self) -> TeamModel:
        return self._game_model.home_team

    @property
    def away_team(self) -> TeamModel:
        return self._game_model.away_team

    @property
    def venue(self) -> Optional[VenueModel]:
        venue = self._game_model.venue
        if venue is not None:
            return AFLCombinedVenueModel(self.session, venue)
        return venue

    @property
    def teams(self) -> Sequence[TeamModel]:
        return [
            AFLCombinedTeamModel(self.session, x, self.dt.date())
            for x in self._game_model.teams
        ]

    @property
    def end_dt(self) -> datetime.datetime | None:
        """Return the end time of the game."""
        return self._game_model.end_dt

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **AFLAFLTablesGameModel.urls_expire_after(),
            **AFLCombinedTeamModel.urls_expire_after(),
            **AFLCombinedVenueModel.urls_expire_after(),
        }
