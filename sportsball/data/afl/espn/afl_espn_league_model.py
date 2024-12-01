"""AFL ESPN league model."""

# pylint: disable=line-too-long
import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League
from .afl_espn_season_model import AFLESPNSeasonModel

_SEASON_URL = "https://sports.core.api.espn.com/v2/sports/australian-football/leagues/afl/seasons?limit=100"


class AFLESPNLeagueModel(ESPNLeagueModel):
    """AFL ESPN implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(_SEASON_URL, League.AFL, session)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **AFLESPNSeasonModel.urls_expire_after(),
            **{
                _SEASON_URL + ".*": datetime.timedelta(hours=1),
            },
        }
