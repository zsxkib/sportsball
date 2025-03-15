"""AFL AFLTables game model."""

# pylint: disable=too-many-arguments
import datetime
import urllib.parse
from urllib.parse import urlparse

import pytest_is_running
import requests_cache
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse

from ....cache import MEMORY
from ...game_model import GameModel
from ...league import League
from ...season_type import SeasonType
from .afl_afltables_team_model import create_afl_afltables_team_model
from .afl_afltables_venue_model import create_afl_afltables_venue_model

_FINALS_WEEK_ADDITION_MAP = {
    "Qualifying Final": 1,
    "Elimination Final": 1,
    "Semi Final": 2,
    "Preliminary Final": 3,
    "Grand Final": 4,
}


def _find_end_dt(
    soup: BeautifulSoup, dt: datetime.datetime
) -> datetime.datetime | None:
    end_dt = None
    for b in soup.find_all("b"):
        b_text = b.get_text().strip()
        if "Game time:" in b_text:
            b_text = b_text[b_text.find("Game time:") :]
            b_text = b_text.replace("Game time:", "")
            if ")" in b_text:
                b_text = b_text[: b_text.find(")")]
            b_text = b_text[: b_text.find("s")]
            min_text, sec_text = b_text.split(" ")[-2:]
            end_dt = dt + datetime.timedelta(
                minutes=int(min_text.replace("m", "")),
                seconds=int(sec_text.replace("s", "").replace(")", "")),
            )
            break
    return end_dt


def _find_team_info(tr: Tag, url: str) -> tuple[str, str, int] | None:
    team_url = None
    team_name = None
    team_points = None
    for a in tr.find_all("a", href=True):
        team_url = urllib.parse.urljoin(url, a.get("href"))
        team_name = a.get_text().strip()
    for b in tr.find_all("b"):
        try:
            team_points = int(b.get_text().strip())
        except ValueError:
            pass
    if team_url is None or team_name is None or team_points is None:
        return None
    return team_url, team_name, team_points


def _find_season_metadata(
    soup: BeautifulSoup,
    url: str,
    last_round_number: int,
) -> tuple[
    datetime.datetime,
    str,
    int,
    list[tuple[str, str, int]],
    datetime.datetime | None,
    int | None,
]:
    # pylint: disable=too-many-locals,too-many-branches
    def _parse_date_text(date_text: str) -> datetime.datetime:
        date_text = td_text[td_text.find("Date:") + 5 :]
        date_text = date_text[: date_text.find("Attendance:")]
        if "(" in date_text:
            date_text = date_text[: date_text.find("(") - 1]
        date_text = date_text.strip()
        return parse(date_text)

    dt = None
    venue_url = None
    week = None
    team_infos: dict[str, tuple[str, int]] = {}
    attendance = None
    for table in soup.find_all("table"):
        for tr in table.find_all("tr"):
            for td in tr.find_all("td"):
                td_text = td.get_text()
                if "Date:" in td_text:
                    dt = _parse_date_text(td_text)
                if "Venue:" in td_text:
                    for a in td.find_all("a", href=True):
                        venue_url = urllib.parse.urljoin(url, a.get("href"))
                if "Round:" in td_text:
                    round_text = td_text[td_text.find("Round:") + 6 :]
                    round_text = round_text[: round_text.find("Venue:")]
                    round_text = round_text.strip()
                    week_addition = _FINALS_WEEK_ADDITION_MAP.get(round_text)
                    if week_addition is None:
                        week = int(round_text)
                    else:
                        week = last_round_number + week_addition
                if "Attendance:" in td_text:
                    attendance_text = td_text[
                        td_text.find("Attendance:") + 11 :
                    ].strip()
                    attendance = int(attendance_text)
            team_info = _find_team_info(tr, url)
            if team_info is not None:
                team_infos[team_info[0]] = (team_info[1], team_info[2])

    if dt is None:
        raise ValueError("dt is null.")
    if venue_url is None:
        raise ValueError("venue_url is null.")
    if week is None:
        raise ValueError("week is null.")
    dt = dt.replace(tzinfo=None)

    return (
        dt,
        venue_url,
        week,
        [(k, v[0], v[1]) for k, v in team_infos.items()],
        _find_end_dt(soup, dt),
        attendance,
    )


def _create_afl_afltables_game_model(
    game_number: int,
    session: requests_cache.CachedSession,
    url: str,
    last_round_number: int,
    last_ladder_ranks: dict[str, int] | None,
    league: League,
    season_year: int | None,
    season_type: SeasonType | None,
) -> GameModel:
    # pylint: disable=too-many-locals
    response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    def _find_teams_metadata(
        soup: BeautifulSoup, team_infos: list[tuple[str, str, int]]
    ) -> list[tuple[str, list[tuple[str, str, int | None]], int]]:
        def _is_correct_table(table: Tag, name: str) -> bool:
            for th in table.find_all("th"):
                header_text = th.get_text().strip()
                if name + " Match Statistics" in header_text:
                    return True
            return False

        def _find_players(table: Tag) -> list[tuple[str, str, int | None]]:
            players: list[tuple[str, str, int | None]] = []
            for tr in table.find_all("tr"):
                player_row = False
                player_url = None
                for a in tr.find_all("a", href=True):
                    player_url = urllib.parse.urljoin(url, a.get("href"))
                    o = urlparse(player_url)
                    if "players" in o.path.split("/"):
                        player_row = True
                if player_row and player_url is not None:
                    jersey = None
                    kicks = None
                    for count, td in enumerate(tr.find_all("td")):
                        if count == 0:
                            jersey = td.get_text().strip()
                        elif count == 2:
                            kicks_text = td.get_text().strip()
                            if kicks_text:
                                kicks = int(kicks_text)

                    if jersey is None:
                        raise ValueError("jersey is null.")

                    players.append((player_url, jersey, kicks))
            return players

        team_metadata = []
        for team_url, name, points in team_infos:
            for table in soup.find_all("table"):
                if _is_correct_table(table, name):
                    players = _find_players(table)
                    team_metadata.append((team_url, players, points))
                    break
        return team_metadata

    dt, venue_url, week, team_infos, end_dt, attendance = _find_season_metadata(
        soup, url, last_round_number
    )
    return GameModel(
        dt=dt,
        week=week,
        game_number=game_number,
        venue=create_afl_afltables_venue_model(venue_url, session, dt),
        teams=[
            create_afl_afltables_team_model(
                team_url,
                players,
                float(points),
                session,  # pyright: ignore
                last_ladder_ranks,
                dt,
                league,
            )
            for team_url, players, points in _find_teams_metadata(soup, team_infos)
        ],
        end_dt=end_dt,
        attendance=attendance,
        league=str(league),
        year=season_year,
        season_type=season_type,
        postponed=None,
        play_off=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_afl_afltables_game_model(
    game_number: int,
    session: requests_cache.CachedSession,
    url: str,
    last_round_number: int,
    last_ladder_ranks: dict[str, int] | None,
    league: League,
    season_year: int | None,
    season_type: SeasonType | None,
) -> GameModel:
    return _create_afl_afltables_game_model(
        game_number,
        session,
        url,
        last_round_number,
        last_ladder_ranks,
        league,
        season_year,
        season_type,
    )


def create_afl_afltables_game_model(
    game_number: int,
    session: requests_cache.CachedSession,
    url: str,
    last_round_number: int,
    last_ladder_ranks: dict[str, int] | None,
    league: League,
    season_year: int | None,
    season_type: SeasonType | None,
    dt: datetime.datetime,
) -> GameModel:
    """Create a game model from AFL Tables."""
    if (
        not pytest_is_running.is_running()
        and dt < datetime.datetime.now() - datetime.timedelta(days=7)
    ):
        return _cached_create_afl_afltables_game_model(
            game_number,
            session,
            url,
            last_round_number,
            last_ladder_ranks,
            league,
            season_year,
            season_type,
        )
    with session.cache_disabled():
        return _create_afl_afltables_game_model(
            game_number,
            session,
            url,
            last_round_number,
            last_ladder_ranks,
            league,
            season_year,
            season_type,
        )
