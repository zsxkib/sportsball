"""NFL ESPN league model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests_cache

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League
from .nfl_espn_season_model import NFLESPNSeasonModel

_SEASON_URL = (
    "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons?limit=100"
)


class NFLESPNLeagueModel(ESPNLeagueModel):
    """NFL ESPN implementation of the league model."""

    def __init__(self, session: requests_cache.CachedSession) -> None:
        super().__init__(_SEASON_URL, League.NFL, session)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **NFLESPNSeasonModel.urls_expire_after(),
            **{
                _SEASON_URL + ".*": datetime.timedelta(hours=1),
            },
        }
