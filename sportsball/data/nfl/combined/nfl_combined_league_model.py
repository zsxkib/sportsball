"""NFL combined league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests

from ...league import League
from ...league_model import LeagueModel
from ...season_model import SeasonModel
from ..espn.nfl_espn_league_model import NFLESPNLeagueModel
from ..sportsdb.nfl_sportsdb_league_model import NFLSportsDBLeagueModel
from .nfl_combined_season_model import NFLCombinedSeasonModel


class NFLCombinedLeagueModel(LeagueModel):
    """NFL combined implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.NFL, session)
        self._espn_league_model = NFLESPNLeagueModel(session)
        self._sportsdb_league_model = NFLSportsDBLeagueModel(session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        seasons: dict[str, list[SeasonModel]] = {}
        for league_model in [self._sportsdb_league_model, self._espn_league_model]:
            for season_model in league_model.seasons:
                key = "-".join([str(season_model.year), str(season_model.season_type)])
                seasons[key] = seasons.get(key, []) + [season_model]
        for v in seasons.values():
            yield NFLCombinedSeasonModel(self._session, v)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **NFLSportsDBLeagueModel.urls_expire_after(),
            **NFLCombinedSeasonModel.urls_expire_after(),
            **NFLESPNLeagueModel.urls_expire_after(),
        }
