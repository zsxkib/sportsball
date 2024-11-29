"""AFL AFLTables game model."""

import datetime
import urllib.parse
from typing import Any, Dict, Optional, Pattern, Sequence, Union
from urllib.parse import urlparse

import requests_cache
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse

from ...game_model import GameModel
from ...team_model import TeamModel
from ...venue_model import VenueModel
from .afl_afltables_team_model import AFLAFLTablesTeamModel
from .afl_afltables_venue_model import AFLAFLTablesVenueModel

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
    int,
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
    if attendance is None:
        raise ValueError("attendance is null.")

    return (
        dt,
        venue_url,
        week,
        [(k, v[0], v[1]) for k, v in team_infos.items()],
        _find_end_dt(soup, dt),
        attendance,
    )


class AFLAFLTablesGameModel(GameModel):
    """AFL AFLTables implementation of the game model."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        url: str,
        session: requests_cache.CachedSession,
        game_number: int,
        last_round_number: int,
    ) -> None:
        super().__init__(session)
        self._game_number = game_number
        response = session.get(url)
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

        self._dt, venue_url, self._week, team_infos, self._end_dt, self._attendance = (
            _find_season_metadata(soup, url, last_round_number)
        )
        self._venue_url = venue_url
        self._teams_info = _find_teams_metadata(soup, team_infos)
        self._venue_model: VenueModel | None = None
        self._teams: Sequence[TeamModel] = []

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        return self._dt

    @property
    def week(self) -> int:
        """Return the game week."""
        return self._week

    @property
    def game_number(self) -> int:
        """Return the game number."""
        return self._game_number

    @property
    def home_team(self) -> TeamModel:
        return self.teams[0]

    @property
    def away_team(self) -> TeamModel:
        return self.teams[1]

    @property
    def venue(self) -> Optional[VenueModel]:
        if self._venue_model is None:
            self._venue_model = AFLAFLTablesVenueModel(self._venue_url, self._session)
        return self._venue_model

    @property
    def teams(self) -> Sequence[TeamModel]:
        if len(self._teams) < len(self._teams_info):
            self._teams = [
                AFLAFLTablesTeamModel(team_url, players, float(points), self._session)
                for team_url, players, points in self._teams_info
            ]
        return self._teams

    @property
    def end_dt(self) -> datetime.datetime | None:
        """Return the end time of the game."""
        return self._end_dt

    @property
    def attendance(self) -> int | None:
        """Return the attendance at the game."""
        return self._attendance

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **AFLAFLTablesVenueModel.urls_expire_after(),
            **AFLAFLTablesTeamModel.urls_expire_after(),
        }
