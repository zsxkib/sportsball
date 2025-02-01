"""Odds Portal league model."""

import json
import urllib.parse
from typing import Iterator

import extruct  # type: ignore
import tqdm
from bs4 import BeautifulSoup, Tag

from ..game_model import GameModel
from ..league import League
from ..league_model import LeagueModel
from .oddsportal_game_model import create_oddsportal_game_model

# Sports
AMERICAN_FOOTBALL = "american-football"
BASKETBALL = "basketball"

# Countries
USA = "usa"

# Leagues
NCAA = "ncaa"


class OddsPortalLeagueModel(LeagueModel):
    """Odds Portal implementation of the league model."""

    @property
    def _path(self) -> str:
        match self.league:
            case League.AFL:
                return "/".join(["aussie-rules", "australia", "afl", ""])
            case League.NBA:
                return "/".join([BASKETBALL, USA, "nba", ""])
            case League.NCAAB:
                return "/".join([BASKETBALL, USA, NCAA, ""])
            case League.NCAAF:
                return "/".join([AMERICAN_FOOTBALL, USA, NCAA, ""])
            case League.NFL:
                return "/".join([AMERICAN_FOOTBALL, USA, "nfl", ""])
            case _:
                raise ValueError(f"Unsupported league: {self.league}")

    def _find_next(self, pbar: tqdm.tqdm) -> Iterator[GameModel]:
        base_url = "https://www.oddsportal.com/" + self._path
        with self.session.cache_disabled():
            response = self.session.get(base_url)
        response.raise_for_status()
        data = extruct.extract(response.text, base_url=base_url)
        for jsonld in data["json-ld"]:
            if jsonld["@type"] != "SportsEvent":
                continue
            game_model = create_oddsportal_game_model(
                self.session,
                urllib.parse.urljoin(base_url, jsonld["url"]),
                self.league,
                True,
            )
            pbar.update(1)
            pbar.set_description(f"OddsPortal {game_model.dt}")
            yield game_model

    def _find_previous(self, pbar: tqdm.tqdm) -> Iterator[GameModel]:
        seen_urls = set()
        queued_urls = {"https://www.oddsportal.com/" + self._path + "results/"}
        while queued_urls:
            url = queued_urls.pop()
            if url in seen_urls:
                continue
            seen_urls.add(url)

            if url.endswith("results/"):
                with self.session.cache_disabled():
                    response = self.session.get(url)
            else:
                response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Find next URLs
            for a in soup.find_all("a", href=True):
                next_url = urllib.parse.urljoin(url, a.get("href"))
                if next_url.endswith("/results/"):
                    queued_urls.add(next_url)

            # Paginate through results
            while True:
                tournament_component = soup.find("tournament-component")
                if not isinstance(tournament_component, Tag):
                    raise ValueError("tournament_component is not a tag.")
                matches = json.loads(str(tournament_component[":sport-data"]))
                component = matches.get("tournamentGamesComponent", matches.get("d"))
                if component.get("total") == 0:
                    break
                for match in component.get("rows", []):
                    game_model = create_oddsportal_game_model(
                        self.session,
                        urllib.parse.urljoin(url, match["url"]),
                        self.league,
                        False,
                    )
                    pbar.update(1)
                    pbar.set_description(f"OddsPortal {game_model.dt}")
                    yield game_model

                next_a = soup.find("a", text="Next", href=True)
                if next_a is None:
                    break
                if not isinstance(next_a, Tag):
                    raise ValueError("next_a is not a tag.")
                next_url = urllib.parse.urljoin(url, str(next_a.get("href")))
                response = self.session.get(next_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

    @property
    def games(self) -> Iterator[GameModel]:
        with tqdm.tqdm() as pbar:
            yield from self._find_next(pbar)
            yield from self._find_previous(pbar)
