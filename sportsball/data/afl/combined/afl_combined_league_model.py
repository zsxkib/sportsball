"""AFL combined league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests_cache

from ...league import League
from ...league_model import LeagueModel
from ...season_model import SeasonModel
from ..afltables.afl_afltables_league_model import AFLAFLTablesLeagueModel
from .afl_combined_season_model import AFLCombinedSeasonModel


class AFLCombinedLeagueModel(LeagueModel):
    """AFL combined implementation of the league model."""

    def __init__(self, session: requests_cache.CachedSession) -> None:
        super().__init__(League.AFL, session)
        self._afltables_league_model = AFLAFLTablesLeagueModel(session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        for season_model in self._afltables_league_model.seasons:
            yield AFLCombinedSeasonModel(self._session, season_model)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **AFLAFLTablesLeagueModel.urls_expire_after(),
            **AFLCombinedSeasonModel.urls_expire_after(),
        }
