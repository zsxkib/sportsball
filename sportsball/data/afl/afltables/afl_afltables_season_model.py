"""AFL AFLTables season model."""

# pylint: disable=line-too-long
import datetime
import os
import urllib.parse
from typing import Any, Dict, Iterator, Optional, Pattern, Union
from urllib.parse import urlparse

import requests_cache
from bs4 import BeautifulSoup

from ...game_model import GameModel
from ...season_model import SeasonModel
from ...season_type import SeasonType
from .afl_afltables_game_model import AFLAFLTablesGameModel


class AFLAFLTablesSeasonModel(SeasonModel):
    """The class implementing the AFL AFLTables season model."""

    def __init__(
        self,
        session: requests_cache.CachedSession,
        season_url: str,
        season_type: SeasonType,
    ) -> None:
        super().__init__(session)
        o = urlparse(season_url)
        last_component = o.path.split("/")[-1]
        filename, _ = os.path.splitext(last_component)
        self._season_url = season_url
        self._year = int(filename)
        self._season_type = season_type

    @property
    def year(self) -> int | None:
        """Return the year."""
        return self._year

    @property
    def season_type(self) -> SeasonType | None:
        """Return the season type."""
        return self._season_type

    @property
    def games(self) -> Iterator[GameModel]:
        response = self._session.get(self._season_url)
        soup = BeautifulSoup(response.text, "html.parser")
        in_finals = False
        game_number = 0
        for table in soup.find_all("table"):
            for b in table.find_all("b"):
                if b.get_text() == "Finals":
                    in_finals = True
            for a in table.find_all("a", href=True):
                if a.get_text().strip().lower() == "match stats":
                    if not in_finals and self.season_type == SeasonType.REGULAR:
                        yield AFLAFLTablesGameModel(
                            urllib.parse.urljoin(self._season_url, a.get("href")),
                            self._session,
                            game_number,
                        )
                    elif in_finals and self.season_type == SeasonType.POSTSEASON:
                        yield AFLAFLTablesGameModel(
                            urllib.parse.urljoin(self._season_url, a.get("href")),
                            self._session,
                            game_number,
                        )
                    game_number += 1

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL caching rules."""
        return {
            **{
                "https://afltables.com/afl/seas/.*": datetime.timedelta(hours=1),
            },
            **AFLAFLTablesGameModel.urls_expire_after(),
        }
