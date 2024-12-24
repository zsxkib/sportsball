"""NFL ESPN league model."""

import requests

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League

_SEASON_URL = (
    "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons?limit=100"
)


class NFLESPNLeagueModel(ESPNLeagueModel):
    """NFL ESPN implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(_SEASON_URL, League.NFL, session)
