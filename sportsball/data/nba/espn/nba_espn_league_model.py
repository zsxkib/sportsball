"""NBA ESPN league model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League
from .nba_espn_season_model import NBAESPNSeasonModel

_SEASON_URL = (
    "http://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons?limit=100"
)


class NBAESPNLeagueModel(ESPNLeagueModel):
    """NBA ESPN implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(_SEASON_URL, League.NBA, session)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **NBAESPNSeasonModel.urls_expire_after(),
            **{
                _SEASON_URL + ".*": datetime.timedelta(hours=1),
            },
        }
