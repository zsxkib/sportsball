"""AFL combined league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests

from ...league import League
from ...league_model import LeagueModel
from ...season_model import SeasonModel
from ..afltables.afl_afltables_league_model import AFLAFLTablesLeagueModel
from ..espn.afl_espn_league_model import AFLESPNLeagueModel
from .afl_combined_season_model import AFLCombinedSeasonModel


class AFLCombinedLeagueModel(LeagueModel):
    """AFL combined implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.AFL, session)
        self._afltables_league_model = AFLAFLTablesLeagueModel(session)
        self._espn_league_model = AFLESPNLeagueModel(session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        seasons: dict[str, list[SeasonModel]] = {}
        for season_model in self._afltables_league_model.seasons:
            key = "-".join([str(season_model.year), str(season_model.season_type)])
            seasons[key] = seasons.get(key, []) + [season_model]
        for season_model in self._espn_league_model.seasons:
            key = "-".join([str(season_model.year), str(season_model.season_type)])
            seasons[key] = seasons.get(key, []) + [season_model]
        for v in seasons.values():
            yield AFLCombinedSeasonModel(self._session, v)

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
            **AFLESPNLeagueModel.urls_expire_after(),
        }
