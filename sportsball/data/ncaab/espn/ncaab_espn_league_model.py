"""NCAAB ESPN league model."""

# pylint: disable=line-too-long
import requests

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League

_SEASON_URL = "http://sports.core.api.espn.com/v2/sports/basketball/leagues/mens-college-basketball?lang=en&region=us"


class NCAABESPNLeagueModel(ESPNLeagueModel):
    """NCAAB ESPN implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(_SEASON_URL, League.NCAAB, session)
