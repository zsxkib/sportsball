"""AFL aussportsbetting league model."""

import requests

from ...aussportsbetting.aussportsbetting_league_model import \
    AusSportsBettingLeagueModel
from ...league import League


class AFLAusSportsBettingLeagueModel(AusSportsBettingLeagueModel):
    """AFL AusSportsBetting implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.AFL, session)
