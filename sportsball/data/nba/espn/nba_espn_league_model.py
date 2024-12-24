"""NBA ESPN league model."""

import requests

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League

_SEASON_URL = (
    "http://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons?limit=100"
)


class NBAESPNLeagueModel(ESPNLeagueModel):
    """NBA ESPN implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(_SEASON_URL, League.NBA, session)
