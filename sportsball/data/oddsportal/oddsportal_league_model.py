"""Odds Portal league model."""

# pylint: disable=too-many-locals,too-many-branches,too-many-statements,protected-access,too-many-arguments,line-too-long,too-many-return-statements,broad-exception-caught
import http
import json
import logging
import urllib.parse
from typing import Iterator

import extruct  # type: ignore
import requests
import tqdm
from bs4 import BeautifulSoup
from scrapesession.scrapesession import ScrapeSession  # type: ignore

from ..game_model import GameModel
from ..google.address_exception import AddressException
from ..league import League
from ..league_model import SHUTDOWN_FLAG, LeagueModel
from .decrypt import fetch_data
from .oddsportal_game_model import create_oddsportal_game_model

# Sports
AMERICAN_FOOTBALL = "american-football"
BASKETBALL = "basketball"

# Countries
USA = "usa"

# Leagues
NCAA = "ncaa"


def _find_ids(text: str) -> tuple[str, str]:
    sentinel = "var pageOutrightsVar = '"
    sanitised_text = text[text.find(sentinel) + len(sentinel) :]
    sanitised_text = sanitised_text[: sanitised_text.find("'")]
    try:
        page_outrights = json.loads(sanitised_text)
    except json.decoder.JSONDecodeError:
        sentinel = "var page = new PageTournament("
        sanitised_text = text[text.find(sentinel) + len(sentinel) :]
        sanitised_text = sanitised_text[: sanitised_text.find(");")]
        try:
            page_outrights = json.loads(sanitised_text)
        except json.decoder.JSONDecodeError as exc:
            logging.error(sanitised_text)
            logging.error(text)
            raise exc
    return str(page_outrights["sid"]), page_outrights["id"]


def _process_results_pages(
    url: str,
    session: ScrapeSession,
    soup: BeautifulSoup,
    league: League,
    pbar: tqdm.tqdm,
    response: requests.Response,
) -> Iterator[GameModel]:
    # Fetch first page
    sports_id, oddsportal_id = _find_ids(response.text)

    current_page = 1
    total_pages = None
    while (current_page == 1 and total_pages is None) or (
        current_page <= (0 if total_pages is None else total_pages)
    ):
        dat_url = f"https://www.oddsportal.com/ajax-sport-country-tournament-archive_/{sports_id}/{oddsportal_id}/X134529032X0X0X0X0X0X0X0X0X0X0X0X0X0X0X0X0X0X512X32X0X0X0X0X0X0X131072X0X2048/1/-5/page/{current_page}//"
        try:
            parsed_data = fetch_data(dat_url, session, url, soup)
            d = parsed_data["d"]
            if d.get("total") == 0:
                return
            for row in d.get("rows", []):
                if SHUTDOWN_FLAG.is_set():
                    return
                game_model = create_oddsportal_game_model(
                    session, urllib.parse.urljoin(url, row["url"]), league, False
                )
                if game_model is None:
                    continue
                pbar.update(1)
                pbar.set_description(f"OddsPortal {game_model.dt}")
                yield game_model
            pagination = d["pagination"]
            total_pages = pagination["pages"]
            current_page += 1
        except AddressException as exc:
            raise exc
        except Exception as exc:
            logging.warning(str(exc))
            break


class OddsPortalLeagueModel(LeagueModel):
    """Odds Portal implementation of the league model."""

    @classmethod
    def name(cls) -> str:
        return "oddsportal-league-model"

    @property
    def _path(self) -> str:
        match self.league:
            case League.AFL:
                return "/".join(["aussie-rules", "australia", "afl", ""])
            case League.EPL:
                return "/".join(["football", "england", "premier-league", ""])
            case League.NBA:
                return "/".join([BASKETBALL, USA, "nba", ""])
            case League.NCAAB:
                return "/".join([BASKETBALL, USA, NCAA, ""])
            case League.NCAAF:
                return "/".join([AMERICAN_FOOTBALL, USA, NCAA, ""])
            case League.NFL:
                return "/".join([AMERICAN_FOOTBALL, USA, "nfl", ""])
            case League.NHL:
                return "/".join(["hockey", USA, "nhl", ""])
            case League.MLB:
                return "/".join(["baseball", USA, "mlb", ""])
            case _:
                raise ValueError(f"Unsupported league: {self.league}")

    def _find_next(self, pbar: tqdm.tqdm) -> Iterator[GameModel]:
        base_url = "https://www.oddsportal.com/" + self._path
        with self.session.cache_disabled():
            with self.session.wayback_disabled():
                response = self.session.get(base_url)
        response.raise_for_status()
        data = extruct.extract(response.text, base_url=base_url)
        for jsonld in data["json-ld"]:
            if jsonld["@type"] != "SportsEvent":
                continue
            try:
                game_model = create_oddsportal_game_model(
                    self.session,
                    urllib.parse.urljoin(base_url, jsonld["url"]),
                    self.league,
                    True,
                )
                if game_model is None:
                    continue
                pbar.update(1)
                pbar.set_description(
                    f"OddsPortal {game_model.year} - {game_model.season_type} - {game_model.dt}"
                )
                yield game_model
            except requests.exceptions.HTTPError as exc:
                if exc.response.status_code == http.HTTPStatus.NOT_FOUND:
                    logging.warning("Failed to find game at: %s", jsonld["url"])
                    continue
                raise exc

    def _find_previous(self, pbar: tqdm.tqdm) -> Iterator[GameModel]:
        standard_suffix = self._path + "results/"
        seen_urls = set()
        queued_urls = {"https://www.oddsportal.com/" + standard_suffix}
        while queued_urls:
            url = queued_urls.pop()
            if url in seen_urls:
                continue
            seen_urls.add(url)

            with self.session.cache_disabled():
                with self.session.wayback_disabled():
                    response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            # Find next URLs
            for option in soup.find_all("option"):
                next_url = urllib.parse.urljoin(url, option.get("value"))
                if next_url.endswith("/results/") and self._path[:-1] in next_url:
                    queued_urls.add(next_url)

            yield from _process_results_pages(
                url,
                self.session,
                soup,
                self.league,
                pbar,
                response,
            )

    @property
    def games(self) -> Iterator[GameModel]:
        try:
            with tqdm.tqdm(position=self.position) as pbar:
                yield from self._find_next(pbar)
                yield from self._find_previous(pbar)
        except Exception as exc:
            SHUTDOWN_FLAG.set()
            raise exc
