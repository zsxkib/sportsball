"""AFL AFLTables league model."""

# pylint: disable=too-many-statements
import datetime
import os
import urllib.parse
from typing import Iterator
from urllib.parse import urlparse

import requests_cache
import tqdm
from bs4 import BeautifulSoup
from dateutil import parser

from ...game_model import GameModel
from ...league import League
from ...league_model import LeagueModel
from ...season_type import SeasonType
from .afl_afltables_game_model import create_afl_afltables_game_model

_SEASON_URL = "https://afltables.com/afl/seas/season_idx.html"


class AFLAFLTablesLeagueModel(LeagueModel):
    """AFL AFLTables implementation of the league model."""

    def __init__(self, session: requests_cache.CachedSession) -> None:
        super().__init__(League.AFL, session)

    def _produce_games(
        self, season_url: str, season_type: SeasonType
    ) -> Iterator[GameModel]:
        # pylint: disable=too-many-branches,too-many-locals
        o = urlparse(season_url)
        last_component = o.path.split("/")[-1]
        filename, _ = os.path.splitext(last_component)
        year = int(filename)

        if year < datetime.datetime.now().year - 1:
            with self.session.cache_disabled():
                response = self.session.get(season_url)
        else:
            response = self.session.get(season_url)

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
            current_dt = None
            for td in table.find_all("td"):
                td_text = td.get_text().strip()
                if "(" in td_text:
                    current_dt = parser.parse(td_text.split("(")[0].strip())
            for a in table.find_all("a", href=True):
                if a.get_text().strip().lower() == "match stats":
                    url = urllib.parse.urljoin(season_url, a.get("href"))
                    if url in urls_duplicates:
                        continue
                    if current_dt is None:
                        raise ValueError("current_dt is null.")
                    if not in_finals and season_type == SeasonType.REGULAR:
                        model = create_afl_afltables_game_model(
                            game_number,
                            self.session,
                            url,
                            last_round_number,
                            last_ladder_ranks,
                            self.league,  # pyright: ignore
                            year,
                            season_type,
                            current_dt,
                        )
                        model_week = model.week
                        if model_week is None:
                            raise ValueError("model_week is null")
                        last_round_number = model_week  # pyright: ignore
                        if season_type == SeasonType.REGULAR:
                            yield model  # pyright: ignore
                    elif in_finals and season_type == SeasonType.POSTSEASON:
                        yield create_afl_afltables_game_model(
                            game_number,
                            self.session,
                            url,
                            last_round_number,
                            None,
                            self.league,  # pyright: ignore
                            year,
                            season_type,
                            current_dt,
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

    @property
    def games(self) -> Iterator[GameModel]:
        response = self.session.get(_SEASON_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        with tqdm.tqdm(desc="AFLTables seasons") as pbar:
            for table in soup.find_all("table"):
                for tr in table.find_all("tr"):
                    for td in tr.find_all("td"):
                        for a in td.find_all("a"):
                            url = urllib.parse.urljoin(_SEASON_URL, a.get("href"))
                            yield from self._produce_games(url, SeasonType.REGULAR)
                            yield from self._produce_games(url, SeasonType.POSTSEASON)
                            pbar.update(2)
