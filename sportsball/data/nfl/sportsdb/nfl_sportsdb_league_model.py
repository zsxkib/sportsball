"""NFL Sports DB league model."""

from ....proxy_session import ProxySession
from ...league import League
from ...sportsdb.sportsdb_league_model import SportsDBLeagueModel


class NFLSportsDBLeagueModel(SportsDBLeagueModel):
    """NFL SportsDB implementation of the league model."""

    def __init__(self, session: ProxySession, position: int | None = None) -> None:
        super().__init__(session, "4391", League.NFL, position=position)

    @classmethod
    def name(cls) -> str:
        return "nfl-sportsdb-league-model"
