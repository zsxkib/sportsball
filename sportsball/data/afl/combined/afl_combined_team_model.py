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
        team_model: TeamModel,
        date: datetime.date,
    ) -> None:
        super().__init__(session)
        self._team_model = team_model
        self._date = date

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._team_model.identifier

    @property
    def name(self) -> str:
        """Return the name."""
        return self._team_model.name

    @property
    def location(self) -> str | None:
        """Return the location."""
        return self._team_model.location

    @property
    def players(self) -> Sequence[PlayerModel]:
        return [
            AFLCombinedPlayerModel(self.session, player)
            for player in self._team_model.players
        ]

    @property
    def odds(self) -> Sequence[OddsModel]:
        """Return the odds."""
        try:
            return [AFLAusSportsBettingOddsModel(self.session, self._date, self.name)]
        except ValueError as e:
            if self._date.year >= 2010:
                raise e
            return []

    @property
    def points(self) -> float | None:
        """Return the points scored in the game."""
        return self._team_model.points

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
