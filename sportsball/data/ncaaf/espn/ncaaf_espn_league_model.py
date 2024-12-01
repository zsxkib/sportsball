"""NCAAF ESPN league model."""

# pylint: disable=line-too-long
import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League
from .ncaaf_espn_season_model import NCAAFESPNSeasonModel

_SEASON_URL = "http://sports.core.api.espn.com/v2/sports/football/leagues/college-football/seasons?limit=100"


class NCAAFESPNLeagueModel(ESPNLeagueModel):
    """NCAAF ESPN implementation of the league model."""

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
            **NCAAFESPNSeasonModel.urls_expire_after(),
            **{
                _SEASON_URL + ".*": datetime.timedelta(hours=1),
            },
        }
