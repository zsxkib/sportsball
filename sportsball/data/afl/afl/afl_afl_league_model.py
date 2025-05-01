"""AFL AFL league model."""

# pylint: disable=too-many-statements,protected-access,too-many-locals,bare-except,too-many-branches
import datetime
import logging
import re
from typing import Iterator

import requests_cache
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from ....playwright import ensure_install
from ...game_model import GameModel
from ...league import League
from ...league_model import LeagueModel
from .afl_afl_game_model import create_afl_afl_game_model


def _parse_game_info(
    html: str, session: requests_cache.CachedSession, ladder: list[str]
) -> Iterator[GameModel]:
    soup = BeautifulSoup(html, "lxml")
    for div in soup.find_all("div", {"class": re.compile(".*js-match-list-item.*")}):
        team_names = []
        for span in div.find_all(
            "span", {"class": re.compile(".*team-lineups__team-name.*")}
        ):
            team_names.append(span.get_text().strip())
        teams_players: list[list[tuple[str, str, str, str]]] = [[], []]
        for div_positions_row in div.find_all(
            "div", {"class": re.compile(".*team-lineups__positions-row.*")}
        ):
            row_players: list[list[tuple[str, str, str, str]]] = [[], []]
            for count, div_team_players in enumerate(
                div_positions_row.find_all(
                    "div",
                    {
                        "class": re.compile(
                            ".*team-lineups__positions-players-container.*"
                        )
                    },
                )
            ):
                team_players: list[tuple[str, str, str, str]] = []
                for a in div_team_players.find_all(
                    "a", {"class": re.compile(".*js-player-profile-link.*")}
                ):
                    player_id = "afl:" + a.get("data-player-id")
                    first_name = a.get("data-first-name")
                    second_name = a.get("data-surname")
                    player_number = None
                    for span_player_number in a.find_all(
                        "span",
                        {"class": re.compile(".*team-lineups__player-number.*")},
                    ):
                        player_number = (
                            span_player_number.get_text()
                            .strip()
                            .replace("[", "")
                            .replace("]", "")
                        )
                    if player_number is None:
                        raise ValueError("player_number is null")
                    team_players.append(
                        (player_id, player_number, first_name, second_name)
                    )
                row_players[count].extend(team_players)
            for count, row_players_list in enumerate(row_players):
                teams_players[count].extend(row_players_list)
        dt = None
        for time in div.find_all(
            "time", {"class": re.compile(".*match-list-alt__header-time.*")}
        ):
            dt = datetime.datetime.fromtimestamp(float(time.get("data-date")) / 1000.0)
        venue_name: str | None = None
        for span in div.find_all(
            "span", {"class": re.compile(".*match-list-alt__header-venue.*")}
        ):
            venue_name = span.get_text().strip().replace(",", "")
        if venue_name is None:
            raise ValueError("venue_name is null")
        if dt is None:
            raise ValueError("dt is null")
        yield create_afl_afl_game_model(
            team_names, teams_players, dt, venue_name, session, ladder
        )


class AFLAFLLeagueModel(LeagueModel):
    """AFL AFL implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(League.AFL, session)

    @property
    def _ladder(self) -> list[str]:
        ladder = []
        ensure_install()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            try:
                page.goto(
                    "https://www.afl.com.au/ladder",
                    wait_until="networkidle",
                    timeout=60000.0,
                )
            except:  # noqa: E722
                logging.warning("Ladder URL timed out.")
            soup = BeautifulSoup(page.content(), "lxml")
            for span in soup.find_all(
                "span", {"class": re.compile(".*stats-table__club-name.*")}
            ):
                team_name = span.get_text().strip()
                if team_name in ladder:
                    continue
                ladder.append(team_name)
        return ladder

    @property
    def games(self) -> Iterator[GameModel]:
        ladder = self._ladder
        ensure_install()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(
                "https://www.afl.com.au/matches/team-lineups", wait_until="networkidle"
            )
            yield from _parse_game_info(page.content(), self.session, ladder)
