"""Combined team model."""

import datetime
from typing import Sequence, Type

import requests

from ..odds_model import OddsModel
from ..player_model import PlayerModel
from ..team_model import TeamModel
from .combined_player_model import CombinedPlayerModel


class CombinedTeamModel(TeamModel):
    """Combined implementation of the team model."""

    def __init__(
        self,
        session: requests.Session,
        team_models: list[TeamModel],
        date: datetime.date,
    ) -> None:
        super().__init__(session)
        self._team_models = team_models
        self._date = date

    @classmethod
    def combined_player_model_class(cls) -> Type[CombinedPlayerModel]:
        """The class representing a combined player model."""
        return CombinedPlayerModel

    @classmethod
    def team_identity_map(cls) -> dict[str, str]:
        """The identity map for combined teams."""
        raise NotImplementedError("team_identity_map not implemented on parent class.")

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self.team_identity_map()[self._team_models[0].identifier]

    @property
    def name(self) -> str:
        """Return the name."""
        return self._team_models[0].name

    @property
    def location(self) -> str | None:
        """Return the location."""
        location = None
        for team_model in self._team_models:
            location = team_model.location
            if location is not None:
                break
        return location

    @property
    def players(self) -> Sequence[PlayerModel]:
        players: dict[str, list[PlayerModel]] = {}
        for team_model in self._team_models:
            for player_model in team_model.players:
                key = player_model.jersey
                if key is None:
                    key = player_model.identifier
                players[key] = players.get(key, []) + [player_model]

        return [
            self.combined_player_model_class()(self.session, v)
            for v in players.values()
        ]

    @property
    def odds(self) -> Sequence[OddsModel]:
        """Return the odds."""
        odds: list[OddsModel] = []
        for team_model in self._team_models:
            odds.extend(team_model.odds)
        return odds

    @property
    def points(self) -> float | None:
        """Return the points scored in the game."""
        points = None
        for team_model in self._team_models:
            points = team_model.points
            if points is not None:
                break
        return points
