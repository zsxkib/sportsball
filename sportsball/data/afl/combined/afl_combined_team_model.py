"""AFL combined team model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import requests_cache

from ...odds_model import OddsModel
from ...player_model import PlayerModel
from ...team_model import TeamModel
from ..afltables.afl_afltables_team_model import AFLAFLTablesTeamModel
from ..aussportsbetting.afl_aussportsbetting_odds_model import \
    AFLAusSportsBettingOddsModel
from .afl_combined_player_model import AFLCombinedPlayerModel


class AFLCombinedTeamModel(TeamModel):
    """AFL AFLTables implementation of the team model."""

    def __init__(
        self,
        session: requests_cache.CachedSession,
        team_models: list[TeamModel],
        date: datetime.date,
    ) -> None:
        super().__init__(session)
        self._team_models = team_models
        self._date = date

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._team_models[0].identifier

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

        return [AFLCombinedPlayerModel(self.session, v) for v in players.values()]

    @property
    def odds(self) -> Sequence[OddsModel]:
        """Return the odds."""
        odds: list[OddsModel] = []
        try:
            odds.append(
                AFLAusSportsBettingOddsModel(self.session, self._date, self.name)
            )
        except ValueError as e:
            if self._date.year >= 2010:
                raise e
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

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **AFLAFLTablesTeamModel.urls_expire_after(),
            **AFLCombinedPlayerModel.urls_expire_after(),
            **AFLAusSportsBettingOddsModel.urls_expire_after(),
        }
