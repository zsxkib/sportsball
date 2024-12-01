"""AFL AFLTables league model."""

import datetime
import urllib.parse
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests
from bs4 import BeautifulSoup

from ...league import League
from ...league_model import LeagueModel
from ...season_model import SeasonModel
from ...season_type import SeasonType
from .afl_afltables_season_model import AFLAFLTablesSeasonModel

_SEASON_URL = "https://afltables.com/afl/seas/season_idx.html"


class AFLAFLTablesLeagueModel(LeagueModel):
    """AFL AFLTables implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.AFL, session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        response = self.session.get(_SEASON_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        for table in soup.find_all("table"):
            for tr in table.find_all("tr"):
                for td in tr.find_all("td"):
                    for a in td.find_all("a"):
                        yield AFLAFLTablesSeasonModel(
                            self._session,
                            urllib.parse.urljoin(_SEASON_URL, a.get("href")),
                            SeasonType.REGULAR,
                        )
                        yield AFLAFLTablesSeasonModel(
                            self._session,
                            urllib.parse.urljoin(_SEASON_URL, a.get("href")),
                            SeasonType.POSTSEASON,
                        )

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **AFLAFLTablesSeasonModel.urls_expire_after(),
            **{
                _SEASON_URL: datetime.timedelta(hours=1),
            },
        }
