"""AFL AFL game model."""

# pylint: disable=too-many-statements,protected-access,too-many-arguments,bare-except,duplicate-code
import datetime
import re

import pytest_is_running
import requests_cache
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright

from ....playwright import ensure_install
from ...game_model import GameModel
from ...league import League
from .afl_afl_team_model import create_afl_afl_team_model
from .afl_afl_venue_model import create_afl_afl_venue_model


def _extract_odds(soup: BeautifulSoup) -> list[float]:
    odds = []
    for span in soup.find_all("span", {"class": "betting-button__money"}):
        odds.append(float(span.get_text().strip().replace("$", "")))
    return odds


def _extract_dt(soup: BeautifulSoup) -> datetime.datetime:
    for div in soup.find_all("div", {"class": re.compile(".*js-match-start-time.*")}):
        start_time = div.get("data-start-time")
        return datetime.datetime.fromisoformat(start_time)
    raise ValueError("Unable to find datetime")


def _parse(html: str) -> tuple[list[float], datetime.datetime]:
    soup = BeautifulSoup(html, "lxml")
    return _extract_odds(soup), _extract_dt(soup)


def create_afl_afl_game_model(
    team_names: list[str],
    players: list[list[tuple[str, str, str, str]]],
    dt: datetime.datetime | None,
    venue_name: str,
    session: requests_cache.CachedSession,
    ladder: list[str],
    url: str | None,
    playwright: Playwright,
) -> GameModel:
    """Create a game model from AFL Tables."""
    odds: list[float] = []
    if url is not None and not pytest_is_running.is_running():
        ensure_install()
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(url, wait_until="networkidle")
        except:  # noqa: E722
            pass
        odds, dt = _parse(page.content())
    if dt is None:
        raise ValueError("dt is null")

    venue_model = create_afl_afl_venue_model(venue_name, session, dt)
    teams = [
        create_afl_afl_team_model(
            x,
            players[count],
            session,
            dt,
            ladder,
            odds[count] if count < len(odds) else None,
        )
        for count, x in enumerate(team_names)
    ]
    return GameModel(
        dt=dt,
        week=None,
        game_number=None,
        venue=venue_model,
        teams=teams,
        end_dt=None,
        attendance=None,
        league=League.AFL,
        year=datetime.datetime.today().year,
        season_type=None,
        postponed=None,
        play_off=None,
    )
