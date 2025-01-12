"""NFL aussportsbetting league model."""

import requests

from ...aussportsbetting.aussportsbetting_league_model import \
    AusSportsBettingLeagueModel
from ...league import League


class NFLAusSportsBettingLeagueModel(AusSportsBettingLeagueModel):
    """NFL AusSportsBetting implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.NFL, session)
