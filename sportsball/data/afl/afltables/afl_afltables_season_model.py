"""AFL AFLTables season model."""

# pylint: disable=line-too-long
import datetime
import os
import urllib.parse
from typing import Any, Dict, Iterator, Optional, Pattern, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from ...game_model import GameModel
from ...season_model import SeasonModel
from ...season_type import SeasonType
from .afl_afltables_game_model import AFLAFLTablesGameModel


class AFLAFLTablesSeasonModel(SeasonModel):
    """The class implementing the AFL AFLTables season model."""

    def __init__(
        self,
        session: requests.Session,
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
        # pylint: disable=too-many-locals,too-many-branches
        response = self._session.get(self._season_url)
        soup = BeautifulSoup(response.text, "html.parser")
        in_finals = False
        game_number = 0
        last_round_number = 0
        urls_duplicates = set()
        last_ladder_ranks: dict[str, int] = {}
        for table in soup.find_all("table"):
            for b in table.find_all("b"):
                if b.get_text() == "Finals":
                    in_finals = True
                    break
            for a in table.find_all("a", href=True):
                if a.get_text().strip().lower() == "match stats":
                    url = urllib.parse.urljoin(self._season_url, a.get("href"))
                    if url in urls_duplicates:
                        continue
                    if not in_finals and self.season_type == SeasonType.REGULAR:
                        model = AFLAFLTablesGameModel(
                            url,
                            self._session,
                            game_number,
                            last_round_number,
                            last_ladder_ranks,
                        )
                        last_round_number = model.week
                        if self.season_type == SeasonType.REGULAR:
                            yield model
                    elif in_finals and self.season_type == SeasonType.POSTSEASON:
                        yield AFLAFLTablesGameModel(
                            url,
                            self._session,
                            game_number,
                            last_round_number,
                            None,
                        )
                    game_number += 1
                    urls_duplicates.add(url)
            ladder_count = None
            for tr in table.find_all("tr"):
                if ladder_count is None:
                    for td in tr.find_all("td"):
                        if (
                            td.get_text().strip().lower()
                            == f"rd {last_round_number} ladder"
                        ):
                            ladder_count = 0
                            last_ladder_ranks = {}
                            break
                else:
                    for td in tr.find_all("td"):
                        team_short_name = td.get_text().strip().upper()
                        if len(team_short_name) > 2 and team_short_name.isalpha():
                            continue
                        ladder_count += 1
                        last_ladder_ranks[team_short_name] = ladder_count
                        break

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
