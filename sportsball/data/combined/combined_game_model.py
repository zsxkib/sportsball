"""Combined game model."""

# pylint: disable=line-too-long
import datetime
from typing import Optional, Sequence, Type

import requests

from ..game_model import GameModel
from ..team_model import TeamModel
from ..venue_model import VenueModel
from .combined_team_model import CombinedTeamModel
from .combined_venue_model import CombinedVenueModel


class CombinedGameModel(GameModel):
    """Combined implementation of the game model."""

    _team_models: list[CombinedTeamModel] | None

    def __init__(self, session: requests.Session, game_models: list[GameModel]) -> None:
        super().__init__(session)
        self._game_models = game_models
        self._team_models = None

    @classmethod
    def combined_team_model_class(cls) -> Type[CombinedTeamModel]:
        """The class representing a combined team model."""
        return CombinedTeamModel

    @classmethod
    def combined_venue_model_class(cls) -> Type[CombinedVenueModel]:
        """The class representing a combined venue model."""
        return CombinedVenueModel

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
        venue_identity_map = self.combined_venue_model_class().venue_identity_map()
        found_venue = False
        for venue_model in venue_models:
            if venue_model.identifier not in venue_identity_map:
                print(
                    f"Cannot map venue identifier {venue_model.identifier} for venue {venue_model.name}"
                )
            else:
                found_venue = True
        if not found_venue:
            return None
        return self.combined_venue_model_class()(self.session, venue_models, self.dt)

    @property
    def teams(self) -> Sequence[TeamModel]:
        team_models = self._team_models
        if team_models is None:
            teams: dict[str, list[TeamModel]] = {}
            team_identity_map = self.combined_team_model_class().team_identity_map()
            for game_model in self._game_models:
                for team_model in game_model.teams:
                    try:
                        key = team_identity_map[team_model.identifier]
                        teams[key] = teams.get(key, []) + [team_model]
                    except KeyError:
                        print(
                            f"Failed to map identifier {team_model.identifier} for team {team_model.name}"
                        )
                        # raise
            team_models = [
                self.combined_team_model_class()(self.session, v, self.dt.date())
                for v in teams.values()
            ]
            self._team_models = team_models
        return team_models

    @property
    def end_dt(self) -> datetime.datetime | None:
        """Return the end time of the game."""
        end_dt = None
        for game_model in self._game_models:
            end_dt = game_model.end_dt
            if end_dt is not None:
                break
        return end_dt
