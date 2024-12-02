"""AFL combined game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import requests

from ...game_model import GameModel
from ...team_model import TeamModel
from ...venue_model import VenueModel
from ..afltables.afl_afltables_game_model import AFLAFLTablesGameModel
from .afl_combined_team_model import AFLCombinedTeamModel
from .afl_combined_venue_model import AFLCombinedVenueModel


class AFLCombinedGameModel(GameModel):
    """AFL combined implementation of the game model."""

    def __init__(self, session: requests.Session, game_models: list[GameModel]) -> None:
        super().__init__(session)
        self._game_models = game_models

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        return self._game_models[0].dt

    @property
    def week(self) -> int:
        """Return the game week."""
        return self._game_models[0].week

    @property
    def game_number(self) -> int:
        """Return the game number."""
        return self._game_models[0].game_number

    @property
    def home_team(self) -> TeamModel:
        return self._game_models[0].home_team

    @property
    def away_team(self) -> TeamModel:
        return self._game_models[0].away_team

    @property
    def venue(self) -> Optional[VenueModel]:
        venue_models = [x.venue for x in self._game_models if x.venue is not None]
        if not venue_models:
            return None
        return AFLCombinedVenueModel(self.session, venue_models, self.dt)

    @property
    def teams(self) -> Sequence[TeamModel]:
        teams: dict[str, list[TeamModel]] = {}
        for game_model in self._game_models:
            for team_model in game_model.teams:
                key = team_model.name
                teams[key] = teams.get(key, []) + [team_model]
        return [
            AFLCombinedTeamModel(self.session, v, self.dt.date())
            for v in teams.values()
        ]

    @property
    def end_dt(self) -> datetime.datetime | None:
        """Return the end time of the game."""
        end_dt = None
        for game_model in self._game_models:
            end_dt = game_model.end_dt
            if end_dt is not None:
                break
        return end_dt

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
