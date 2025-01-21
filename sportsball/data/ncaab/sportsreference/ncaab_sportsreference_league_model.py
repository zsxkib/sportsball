"""NCAAB sports reference league model."""

import urllib.parse
from typing import Iterator

import requests
from bs4 import BeautifulSoup, Tag

from ...game_model import GameModel
from ...league import League
from ...league_model import LeagueModel
from .ncaab_sportsreference_game_model import \
    create_ncaab_sportsreference_game_model


class NCAABSportsReferenceLeagueModel(LeagueModel):
    """NCAAB Sports Reference implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.NCAAB, session)

    @property
    def games(self) -> Iterator[GameModel]:
        final_path: str | None = ""
        while final_path is not None:
            url = "https://www.sports-reference.com/cbb/boxscores/" + final_path
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for div in soup.find_all("div", class_="gender-m"):
                for td in div.find_all("td", class_="gamelink"):
                    for a in td.find_all("a"):
                        game_url = urllib.parse.urljoin(url, a.get("href"))
                        yield create_ncaab_sportsreference_game_model(
                            self.session, game_url, self.league
                        )
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
