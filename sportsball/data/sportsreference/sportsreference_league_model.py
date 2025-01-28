"""Sports reference league model."""

# pylint: disable=line-too-long
import datetime
import urllib.parse
from typing import Any, Iterator
from urllib.parse import parse_qs, urlparse

import requests_cache
import tqdm
from bs4 import BeautifulSoup, Tag

from ..game_model import GameModel
from ..league import League
from ..league_model import LeagueModel
from .sportsreference_game_model import create_sportsreference_game_model


class SportsReferenceLeagueModel(LeagueModel):
    """Sports Reference implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, league: League, base_url: str
    ) -> None:
        super().__init__(league, session)
        self._base_url = base_url

    @property
    def games(self) -> Iterator[GameModel]:
        # pylint: disable=too-many-locals
        def _produce_games(
            div: Any, pbar: tqdm.tqdm, dt: datetime.datetime
        ) -> Iterator[GameModel]:
            for td in div.find_all("td", class_="gamelink"):
                for a in td.find_all("a"):
                    pbar.update(1)
                    game_url = urllib.parse.urljoin(url, a.get("href"))
                    game_model = create_sportsreference_game_model(
                        self.session, game_url, self.league, dt
                    )
                    pbar.set_description(
                        f"SportsReference {game_model.year} - {game_model.season_type} - {game_model.dt}"
                    )
                    yield game_model

        final_path: str | None = ""
        with tqdm.tqdm() as pbar:
            while final_path is not None:
                url = self._base_url + final_path
                if final_path:
                    response = self.session.get(url)
                else:
                    with self.session.cache_disabled():
                        response = self.session.get(url)
                response.raise_for_status()
                dt = datetime.datetime.now()
                if final_path:
                    parsed_url = urlparse(url)
                    query = parse_qs(parsed_url.query)
                    dt = datetime.datetime(
                        int(query["year"][0]),
                        int(query["month"][0]),
                        int(query["day"][0]),
                    )
                soup = BeautifulSoup(response.text, "html.parser")
                if self.league == League.NCAAB:
                    for div in soup.find_all("div", class_="gender-m"):
                        yield from _produce_games(div, pbar, dt)
                else:
                    yield from _produce_games(soup, pbar, dt)
                prev_a = soup.find("a", class_="prev")
                if isinstance(prev_a, Tag):
                    href = prev_a.get("href")
                    if isinstance(href, str):
                        prev_url = urllib.parse.urljoin(url, href)
                        final_path = prev_url.split("/")[-1]
                    else:
                        final_path = None
                else:
                    final_path = None
