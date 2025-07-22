"""Sports Reference game model."""

# pylint: disable=too-many-locals,too-many-statements,unused-argument,protected-access,too-many-arguments,use-maxsplit-arg,too-many-branches,duplicate-code,broad-exception-caught,too-many-lines
import datetime
import io
import logging
import os
import re
import urllib.parse
from typing import Any

import datefinder  # type: ignore
import dateutil
import pandas as pd
import pytest_is_running
import requests
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse
from scrapesession.scrapesession import ScrapeSession  # type: ignore

from ...cache import MEMORY
from ..game_model import VERSION, GameModel
from ..league import League
from ..season_type import SeasonType
from ..team_model import TeamModel
from .sportsreference_team_model import create_sportsreference_team_model
from .sportsreference_venue_model import create_sportsreference_venue_model

_MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
_NUMBER_PARENTHESIS_PATTERN = r"\(\d+\)"
_NON_WAYBACK_URLS: set[str] = {
    "https://www.sports-reference.com/cfb/boxscores/2025-01-20-notre-dame.html",
    "https://www.pro-football-reference.com/boxscores/202502090phi.htm",
}


def _find_old_dt(
    dfs: list[pd.DataFrame],
    session: ScrapeSession,
    soup: BeautifulSoup,
    url: str,
    league: League,
    player_urls: set[str],
    fg: dict[str, int],
    fga: dict[str, int],
    offensive_rebounds: dict[str, int],
    assists: dict[str, int],
    turnovers: dict[str, int],
    response: requests.Response,
    positions_validator: dict[str, str],
    minutes_played: dict[str, datetime.timedelta],
    three_point_field_goals: dict[str, int],
    three_point_field_goals_attempted: dict[str, int],
    free_throws: dict[str, int],
    free_throws_attempted: dict[str, int],
    defensive_rebounds: dict[str, int],
    steals: dict[str, int],
    blocks: dict[str, int],
    personal_fouls: dict[str, int],
    player_points: dict[str, int],
    game_scores: dict[str, float],
    point_differentials: dict[str, int],
    goals: dict[str, int],
    penalties_in_minutes: dict[str, datetime.timedelta],
    even_strength_goals: dict[str, int],
    power_play_goals: dict[str, int],
    short_handed_goals: dict[str, int],
    game_winning_goals: dict[str, int],
    even_strength_assists: dict[str, int],
    power_play_assists: dict[str, int],
    short_handed_assists: dict[str, int],
    shots_on_goal: dict[str, int],
    shooting_percentage: dict[str, float],
    shifts: dict[str, int],
    time_on_ice: dict[str, datetime.timedelta],
    decision: dict[str, str],
    goals_against: dict[str, int],
    shots_against: dict[str, int],
    saves: dict[str, int],
    save_percentage: dict[str, float],
    shutouts: dict[str, int],
    individual_corsi_for_events: dict[str, int],
    on_shot_ice_for_events: dict[str, int],
    on_shot_ice_against_events: dict[str, int],
    corsi_for_percentage: dict[str, float],
    relative_corsi_for_percentage: dict[str, float],
    offensive_zone_starts: dict[str, int],
    defensive_zone_starts: dict[str, int],
    offensive_zone_start_percentage: dict[str, float],
    hits: dict[str, int],
    true_shooting_percentage: dict[str, float],
    at_bats: dict[str, int],
    runs_scored: dict[str, int],
    runs_batted_in: dict[str, int],
    bases_on_balls: dict[str, int],
    strikeouts: dict[str, int],
    plate_appearances: dict[str, int],
    hits_at_bats: dict[str, float],
    obp: dict[str, float],
    slg: dict[str, float],
    ops: dict[str, float],
    pitches: dict[str, int],
    strikes: dict[str, int],
    win_probability_added: dict[str, float],
    average_leverage_index: dict[str, float],
    wpa_plus: dict[str, float],
    wpa_minus: dict[str, float],
    cwpa: dict[str, float],
    acli: dict[str, float],
    re24: dict[str, float],
    putouts: dict[str, int],
    innings_pitched: dict[str, int],
    earned_runs: dict[str, int],
    home_runs: dict[str, int],
    era: dict[str, float],
    batters_faced: dict[str, int],
    strikes_by_contact: dict[str, int],
    strikes_swinging: dict[str, int],
    strikes_looking: dict[str, int],
    ground_balls: dict[str, int],
    fly_balls: dict[str, int],
    line_drives: dict[str, int],
    inherited_runners: dict[str, int],
    inherited_scores: dict[str, int],
    effective_field_goal_percentage: dict[str, float],
) -> tuple[datetime.datetime, list[TeamModel], str | None]:
    teams: list[TeamModel] = []

    def _process_team_row(df: pd.DataFrame):
        team_rows = [str(df.iat[0, x]) for x in range(len(df.columns.values))]
        team_rows = [x for x in team_rows if x != "nan"]
        if len(team_rows) == 1:
            team_row = team_rows[0]
            for sentinel in ["Next Game", "Prev Game"]:
                if sentinel in team_row:
                    team_rows = [
                        team_row[: team_row.find(sentinel) + len(sentinel)].strip(),
                        team_row[team_row.find(sentinel) + len(sentinel) :]
                        .strip()
                        .replace("/ Next Game ⇒", "")
                        .replace("⇒", "")
                        .strip(),
                    ]
                    last_splits = team_rows[1].split()
                    if last_splits:
                        if last_splits[0] in _MONTHS:
                            continue
                    break
            if not team_rows[1]:
                sentinel = "Next Game"
                team_rows = [
                    team_row[: team_row.find(sentinel) + len(sentinel)].strip(),
                    team_row[team_row.find(sentinel) + len(sentinel) :]
                    .strip()
                    .replace("⇒", "")
                    .strip(),
                ]
            if not team_rows[1]:
                sentinel = "Prev Game"
                team_rows = [
                    team_row[: team_row.find(sentinel) + len(sentinel)].strip(),
                    team_row[team_row.find(sentinel) + len(sentinel) :]
                    .strip()
                    .replace("⇒", "")
                    .strip(),
                ]
        for team_row in team_rows:
            if team_row.startswith("⇒"):
                team_row = team_row[1:]
            team_row = team_row.strip()
            if "Prev Game" in team_row:
                team_name_points = (
                    team_row.split("⇐")[0]
                    .strip()
                    .replace("Prev Game", "")
                    # .replace("/", "")
                    .strip()
                )
            else:
                team_name_points = (
                    team_row.split("⇒")[0].replace("Next Game", "").strip()
                )
            # Handle team name points like "Indiana Pacers 97 45-37 (Won 3)"
            if "-" in team_name_points:
                dash_splits = team_name_points.split("-")
                # Handle team name points like "Kansas City-Omaha Kings 89"
                # and cases like "Kansas City-Omaha Kings 95 44-38 (Won 1) ⇐ Prev Game"
                for i in range(len(dash_splits) - 1):
                    if (
                        dash_splits[i].split()[-1].isdigit()
                        and dash_splits[i + 1].split()[0].isdigit()
                    ):
                        team_name_points = " ".join(
                            "-".join(dash_splits[: i + 1]).strip().split()[:-1]
                        )
                        break
            for marker in ["Lost", "Won"]:
                team_name_points = team_name_points.split(marker)[0].strip()
            points = int(team_name_points.split()[-1].strip())
            team_name = " ".join(team_name_points.split()[:-1]).strip()
            if " at " in team_name:
                team_name = team_name.split(" at ")[0].strip()
            if " vs " in team_name:
                team_name = team_name.split(" vs ")[0].strip()
            for month in _MONTHS:
                month_split = " " + month + " "
                if month_split in team_name:
                    team_name = team_name.split(month_split)[0].strip()
                    points = int(team_name.split()[-1].strip())
                    team_name = " ".join(team_name.split()[:-1]).strip()
                    break
            team_name = " ".join(
                re.sub(_NUMBER_PARENTHESIS_PATTERN, "", team_name).split()
            ).strip()
            team_a = soup.find("a", text=team_name, href=True)
            if not isinstance(team_a, Tag):
                logging.error(team_name)
                logging.error(response.url)
                logging.error(response.text)
                raise ValueError("team_a is not a tag.")
            team_url = urllib.parse.urljoin(url, str(team_a.get("href")))
            if dt is None:
                raise ValueError("dt is null.")
            teams.append(
                create_sportsreference_team_model(
                    session=session,
                    url=team_url,
                    dt=dt,
                    league=league,
                    player_urls=player_urls,
                    points=points,
                    fg=fg,
                    fga=fga,
                    offensive_rebounds=offensive_rebounds,
                    assists=assists,
                    turnovers=turnovers,
                    team_name=team_name,
                    positions_validator=positions_validator,
                    minutes_played=minutes_played,
                    three_point_field_goals=three_point_field_goals,
                    three_point_field_goals_attempted=three_point_field_goals_attempted,
                    free_throws=free_throws,
                    free_throws_attempted=free_throws_attempted,
                    defensive_rebounds=defensive_rebounds,
                    steals=steals,
                    blocks=blocks,
                    personal_fouls=personal_fouls,
                    player_points=player_points,
                    game_scores=game_scores,
                    point_differentials=point_differentials,
                    goals=goals,
                    penalties_in_minutes=penalties_in_minutes,
                    even_strength_goals=even_strength_goals,
                    power_play_goals=power_play_goals,
                    short_handed_goals=short_handed_goals,
                    game_winning_goals=game_winning_goals,
                    even_strength_assists=even_strength_assists,
                    power_play_assists=power_play_assists,
                    short_handed_assists=short_handed_assists,
                    shots_on_goal=shots_on_goal,
                    shooting_percentage=shooting_percentage,
                    shifts=shifts,
                    time_on_ice=time_on_ice,
                    decision=decision,
                    goals_against=goals_against,
                    shots_against=shots_against,
                    saves=saves,
                    save_percentage=save_percentage,
                    shutouts=shutouts,
                    individual_corsi_for_events=individual_corsi_for_events,
                    on_shot_ice_for_events=on_shot_ice_for_events,
                    on_shot_ice_against_events=on_shot_ice_against_events,
                    corsi_for_percentage=corsi_for_percentage,
                    relative_corsi_for_percentage=relative_corsi_for_percentage,
                    offensive_zone_starts=offensive_zone_starts,
                    defensive_zone_starts=defensive_zone_starts,
                    offensive_zone_start_percentage=offensive_zone_start_percentage,
                    hits=hits,
                    true_shooting_percentage=true_shooting_percentage,
                    at_bats=at_bats,
                    runs_scored=runs_scored,
                    runs_batted_in=runs_batted_in,
                    bases_on_balls=bases_on_balls,
                    strikeouts=strikeouts,
                    plate_appearances=plate_appearances,
                    hits_at_bats=hits_at_bats,
                    obp=obp,
                    slg=slg,
                    ops=ops,
                    pitches=pitches,
                    strikes=strikes,
                    win_probability_added=win_probability_added,
                    average_leverage_index=average_leverage_index,
                    wpa_plus=wpa_plus,
                    wpa_minus=wpa_minus,
                    cwpa=cwpa,
                    acli=acli,
                    re24=re24,
                    putouts=putouts,
                    innings_pitched=innings_pitched,
                    earned_runs=earned_runs,
                    home_runs=home_runs,
                    era=era,
                    batters_faced=batters_faced,
                    strikes_by_contact=strikes_by_contact,
                    strikes_swinging=strikes_swinging,
                    strikes_looking=strikes_looking,
                    ground_balls=ground_balls,
                    fly_balls=fly_balls,
                    line_drives=line_drives,
                    inherited_runners=inherited_runners,
                    inherited_scores=inherited_scores,
                    effective_field_goal_percentage=effective_field_goal_percentage,
                )
            )

    dt = None
    venue_name = None
    for df in dfs:
        if len(df) == 2:
            test_row = df.iat[0, 0]
            test_row_2 = df.iat[1, 0]
            if isinstance(test_row, float):
                continue

            try:
                if (
                    "Prev Game" in test_row
                    or "Next Game" in test_row
                    or "Lost" in test_row
                    or "PM," in test_row_2
                ):
                    date_venue_split = df.iat[1, 0].split()
                    current_idx = 5
                    try:
                        dt = parse(" ".join(date_venue_split[:current_idx]))
                    except dateutil.parser._parser.ParserError:  # type: ignore
                        try:
                            current_idx = 3
                            dt = parse(" ".join(date_venue_split[:current_idx]))
                        except dateutil.parser._parser.ParserError:  # type: ignore
                            dt = parse(
                                " ".join(",".join(test_row.split(",")[1:]).split()[:3])
                            )
                    venue_name = " ".join(date_venue_split[current_idx:])
                    _process_team_row(df)
                    break
            except TypeError as exc:
                logging.error(test_row)
                logging.error(response.url)
                logging.error(response.text)
                raise exc

    if dt is None:
        title_tag = soup.find("title")
        if not isinstance(title_tag, Tag):
            raise ValueError("title_tag is not a tag.")
        title = title_tag.get_text().strip().split("|")[0].strip()
        date = title[title.find(",") :].strip()
        dt = parse(date)
        for df in dfs:
            test_row = df.iat[0, 0]
            if isinstance(test_row, float):
                continue
            try:
                if "Prev Game" in test_row:
                    _process_team_row(df)
                    break
            except TypeError as exc:
                logging.error(test_row)
                logging.error(response.url)
                logging.error(response.text)
                raise exc

    if venue_name is not None and not venue_name.replace(",", "").strip():
        venue_name = None

    if dt is None:
        raise ValueError("dt is null.")
    if venue_name is None:
        logging.warning("venue_name is null for %s.", url)

    return (dt, teams, venue_name)


def _find_new_dt(
    soup: BeautifulSoup,
    scorebox_meta_div: Tag,
    url: str,
    session: ScrapeSession,
    league: League,
    player_urls: set[str],
    scores: list[float],
    fg: dict[str, int],
    fga: dict[str, int],
    offensive_rebounds: dict[str, int],
    assists: dict[str, int],
    turnovers: dict[str, int],
    positions_validator: dict[str, str],
    minutes_played: dict[str, datetime.timedelta],
    three_point_field_goals: dict[str, int],
    three_point_field_goals_attempted: dict[str, int],
    free_throws: dict[str, int],
    free_throws_attempted: dict[str, int],
    defensive_rebounds: dict[str, int],
    steals: dict[str, int],
    blocks: dict[str, int],
    personal_fouls: dict[str, int],
    player_points: dict[str, int],
    game_scores: dict[str, float],
    point_differentials: dict[str, int],
    goals: dict[str, int],
    penalties_in_minutes: dict[str, datetime.timedelta],
    even_strength_goals: dict[str, int],
    power_play_goals: dict[str, int],
    short_handed_goals: dict[str, int],
    game_winning_goals: dict[str, int],
    even_strength_assists: dict[str, int],
    power_play_assists: dict[str, int],
    short_handed_assists: dict[str, int],
    shots_on_goal: dict[str, int],
    shooting_percentage: dict[str, float],
    shifts: dict[str, int],
    time_on_ice: dict[str, datetime.timedelta],
    decision: dict[str, str],
    goals_against: dict[str, int],
    shots_against: dict[str, int],
    saves: dict[str, int],
    save_percentage: dict[str, float],
    shutouts: dict[str, int],
    individual_corsi_for_events: dict[str, int],
    on_shot_ice_for_events: dict[str, int],
    on_shot_ice_against_events: dict[str, int],
    corsi_for_percentage: dict[str, float],
    relative_corsi_for_percentage: dict[str, float],
    offensive_zone_starts: dict[str, int],
    defensive_zone_starts: dict[str, int],
    offensive_zone_start_percentage: dict[str, float],
    hits: dict[str, int],
    true_shooting_percentage: dict[str, float],
    at_bats: dict[str, int],
    runs_scored: dict[str, int],
    runs_batted_in: dict[str, int],
    bases_on_balls: dict[str, int],
    strikeouts: dict[str, int],
    plate_appearances: dict[str, int],
    hits_at_bats: dict[str, float],
    obp: dict[str, float],
    slg: dict[str, float],
    ops: dict[str, float],
    pitches: dict[str, int],
    strikes: dict[str, int],
    win_probability_added: dict[str, float],
    average_leverage_index: dict[str, float],
    wpa_plus: dict[str, float],
    wpa_minus: dict[str, float],
    cwpa: dict[str, float],
    acli: dict[str, float],
    re24: dict[str, float],
    putouts: dict[str, int],
    innings_pitched: dict[str, int],
    earned_runs: dict[str, int],
    home_runs: dict[str, int],
    era: dict[str, float],
    batters_faced: dict[str, int],
    strikes_by_contact: dict[str, int],
    strikes_swinging: dict[str, int],
    strikes_looking: dict[str, int],
    ground_balls: dict[str, int],
    fly_balls: dict[str, int],
    line_drives: dict[str, int],
    inherited_runners: dict[str, int],
    inherited_scores: dict[str, int],
    effective_field_goal_percentage: dict[str, float],
) -> tuple[datetime.datetime, list[TeamModel], str]:
    in_divs = scorebox_meta_div.find_all("div")
    current_in_div_idx = 0
    in_div = in_divs[current_in_div_idx]
    in_div_text = in_div.get_text().strip()
    current_in_div_idx += 1
    if "Tournament" in in_div_text:
        in_div_text = in_divs[1].get_text().strip()
        current_in_div_idx += 1
    dt = None
    try:
        dt = parse(in_div_text)
    except dateutil.parser._parser.ParserError as exc:  # type: ignore
        matches = datefinder.find_dates(scorebox_meta_div.get_text(separator="\n"))
        for match in matches:
            if isinstance(match, datetime.datetime):
                dt = match
                break
        if dt is None:
            logging.error("Failed to parse date for URL: %s", url)
            raise exc
    venue_div = in_divs[current_in_div_idx]
    venue_name = venue_div.get_text().strip()
    if league == League.NCAAF:
        filepath = url.split("/")[-1]
        filename, _ = os.path.splitext(filepath)
        venue_name = "-".join(filename.split("-")[3:])
    else:
        for in_div in in_divs:
            in_div_text = in_div.get_text()
            if "Arena:" in in_div_text:
                venue_name = in_div_text.replace("Arena: ", "").strip()
            elif "Stadium:" in in_div_text:
                venue_name = in_div_text.replace("Stadium: ", "").strip()
            elif "Venue:" in in_div_text:
                venue_name = in_div_text.replace("Venue: ", "").strip()

    scorebox_div = soup.find("div", class_="scorebox")
    if not isinstance(scorebox_div, Tag):
        raise ValueError("scorebox_div is not a Tag.")

    teams: list[TeamModel] = []
    for a in scorebox_div.find_all("a"):
        team_url = urllib.parse.urljoin(url, a.get("href"))
        if "/schools/" in team_url or "/teams/" in team_url:
            teams.append(
                create_sportsreference_team_model(
                    session=session,
                    url=team_url,
                    dt=dt,
                    league=league,
                    player_urls=player_urls,
                    points=scores[len(teams)],
                    fg=fg,
                    fga=fga,
                    offensive_rebounds=offensive_rebounds,
                    assists=assists,
                    turnovers=turnovers,
                    team_name=a.get_text().strip(),
                    positions_validator=positions_validator,
                    minutes_played=minutes_played,
                    three_point_field_goals=three_point_field_goals,
                    three_point_field_goals_attempted=three_point_field_goals_attempted,
                    free_throws=free_throws,
                    free_throws_attempted=free_throws_attempted,
                    defensive_rebounds=defensive_rebounds,
                    steals=steals,
                    blocks=blocks,
                    personal_fouls=personal_fouls,
                    player_points=player_points,
                    game_scores=game_scores,
                    point_differentials=point_differentials,
                    goals=goals,
                    penalties_in_minutes=penalties_in_minutes,
                    even_strength_goals=even_strength_goals,
                    power_play_goals=power_play_goals,
                    short_handed_goals=short_handed_goals,
                    game_winning_goals=game_winning_goals,
                    even_strength_assists=even_strength_assists,
                    power_play_assists=power_play_assists,
                    short_handed_assists=short_handed_assists,
                    shots_on_goal=shots_on_goal,
                    shooting_percentage=shooting_percentage,
                    shifts=shifts,
                    time_on_ice=time_on_ice,
                    decision=decision,
                    goals_against=goals_against,
                    shots_against=shots_against,
                    saves=saves,
                    save_percentage=save_percentage,
                    shutouts=shutouts,
                    individual_corsi_for_events=individual_corsi_for_events,
                    on_shot_ice_for_events=on_shot_ice_for_events,
                    on_shot_ice_against_events=on_shot_ice_against_events,
                    corsi_for_percentage=corsi_for_percentage,
                    relative_corsi_for_percentage=relative_corsi_for_percentage,
                    offensive_zone_starts=offensive_zone_starts,
                    defensive_zone_starts=defensive_zone_starts,
                    offensive_zone_start_percentage=offensive_zone_start_percentage,
                    hits=hits,
                    true_shooting_percentage=true_shooting_percentage,
                    at_bats=at_bats,
                    runs_scored=runs_scored,
                    runs_batted_in=runs_batted_in,
                    bases_on_balls=bases_on_balls,
                    strikeouts=strikeouts,
                    plate_appearances=plate_appearances,
                    hits_at_bats=hits_at_bats,
                    obp=obp,
                    slg=slg,
                    ops=ops,
                    pitches=pitches,
                    strikes=strikes,
                    win_probability_added=win_probability_added,
                    average_leverage_index=average_leverage_index,
                    wpa_plus=wpa_plus,
                    wpa_minus=wpa_minus,
                    cwpa=cwpa,
                    acli=acli,
                    re24=re24,
                    putouts=putouts,
                    innings_pitched=innings_pitched,
                    earned_runs=earned_runs,
                    home_runs=home_runs,
                    era=era,
                    batters_faced=batters_faced,
                    strikes_by_contact=strikes_by_contact,
                    strikes_swinging=strikes_swinging,
                    strikes_looking=strikes_looking,
                    ground_balls=ground_balls,
                    fly_balls=fly_balls,
                    line_drives=line_drives,
                    inherited_runners=inherited_runners,
                    inherited_scores=inherited_scores,
                    effective_field_goal_percentage=effective_field_goal_percentage,
                )
            )

    return (dt, teams, venue_name)


def _create_sportsreference_game_model(
    session: ScrapeSession,
    url: str,
    league: League,
    positions_validator: dict[str, str],
    version: str,
) -> GameModel | None:
    # pylint: disable=too-many-branches
    if url in _NON_WAYBACK_URLS:
        with session.wayback_disabled():
            response = session.get(url)
    else:
        response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    page_title = soup.find("h1", class_="page_title")

    # If the page_title is bad, try fetching from a non wayback source
    if page_title is not None:
        if "file not found" in page_title.get_text().strip().lower():
            session.cache.delete(urls=[url, response.url])
            with session.wayback_disabled():
                response = session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

    player_urls = set()
    for a in soup.find_all("a"):
        player_url = urllib.parse.urljoin(url, a.get("href"))
        if "/players/" in player_url and not player_url.endswith("/players/"):
            player_urls.add(player_url)

    scores = []
    for score_div in soup.find_all("div", class_="score"):
        try:
            scores.append(float(score_div.get_text().strip()))
        except ValueError as exc:
            session.cache.delete(urls=[url, response.url])
            logging.error(response.text)
            raise exc

    def _normalize_value(value: Any) -> Any:
        if isinstance(value, str):
            if "%" in value:
                return float(value.replace("%", ""))
        return value

    handle = io.StringIO()
    handle.write(response.text)
    handle.seek(0)
    fg = {}
    fga = {}
    offensive_rebounds = {}
    assists = {}
    turnovers = {}
    minutes_played = {}
    three_point_field_goals = {}
    three_point_field_goals_attempted = {}
    free_throws = {}
    free_throws_attempted = {}
    defensive_rebounds = {}
    steals = {}
    blocks = {}
    personal_fouls = {}
    player_points = {}
    game_scores = {}
    point_differentials = {}
    goals = {}
    penalties_in_minutes: dict[str, datetime.timedelta] = {}
    even_strength_goals = {}
    power_play_goals = {}
    short_handed_goals = {}
    game_winning_goals = {}
    even_strength_assists: dict[str, int] = {}
    power_play_assists: dict[str, int] = {}
    short_handed_assists: dict[str, int] = {}
    shots_on_goal = {}
    shooting_percentage = {}
    shifts = {}
    time_on_ice = {}
    decision = {}
    goals_against = {}
    shots_against = {}
    saves = {}
    save_percentage = {}
    shutouts = {}
    individual_corsi_for_events = {}
    on_shot_ice_for_events = {}
    on_shot_ice_against_events = {}
    corsi_for_percentage = {}
    relative_corsi_for_percentage = {}
    offensive_zone_starts = {}
    defensive_zone_starts = {}
    offensive_zone_start_percentage = {}
    hits = {}
    true_shooting_percentage = {}
    at_bats = {}
    runs_scored = {}
    runs_batted_in = {}
    bases_on_balls = {}
    strikeouts = {}
    plate_appearances = {}
    hits_at_bats = {}
    obp = {}
    slg = {}
    ops = {}
    pitches = {}
    strikes = {}
    win_probability_added = {}
    average_leverage_index = {}
    wpa_plus = {}
    wpa_minus = {}
    cwpa = {}
    acli = {}
    re24 = {}
    putouts = {}
    innings_pitched = {}
    earned_runs = {}
    home_runs = {}
    era = {}
    batters_faced = {}
    strikes_by_contact = {}
    strikes_swinging = {}
    strikes_looking = {}
    ground_balls = {}
    fly_balls = {}
    line_drives = {}
    inherited_runners = {}
    inherited_scores = {}
    effective_field_goal_percentage = {}
    try:
        dfs = pd.read_html(handle)
        for df in dfs:
            if df.index.nlevels > 1:
                df.columns = df.columns.get_level_values(1)
            cols = set(df.columns.values.tolist())
            players = []
            if "Starters" in cols:
                players = df["Starters"].tolist()
            elif "Batting" in cols:
                players = df["Batting"].tolist()
            elif "Pitching" in cols:
                players = df["Pitching"].tolist()
            elif "Player" in cols:
                players = df["Player"].tolist()
            elif "Reserves" in cols:
                players = df["Reserves"].tolist()

            if players:
                if "FG" in cols:
                    fgs = df["FG"].tolist()
                    for idx, player in enumerate(players):
                        fg[player] = _normalize_value(fgs[idx])
                if "FGA" in cols:
                    fgas = df["FGA"].tolist()
                    for idx, player in enumerate(players):
                        fga[player] = _normalize_value(fgas[idx])
                if "OREB" in cols:
                    orebs = df["OREB"].tolist()
                    for idx, player in enumerate(players):
                        offensive_rebounds[player] = _normalize_value(orebs[idx])
                if "AST" in cols:
                    asts = df["AST"].tolist()
                    for idx, player in enumerate(players):
                        assists[player] = _normalize_value(asts[idx])
                if "TOV" in cols:
                    tovs = df["TOV"].tolist()
                    for idx, player in enumerate(players):
                        turnovers[player] = _normalize_value(tovs[idx])
                if "MP" in cols:
                    mps = df["MP"].tolist()
                    for idx, player in enumerate(players):
                        mp = mps[idx]
                        mp_minutes, mp_seconds = mp.split(":")
                        minutes_played[player] = datetime.timedelta(
                            minutes=int(mp_minutes), seconds=int(mp_seconds)
                        )
                if "3P" in cols:
                    threeps = df["3P"].tolist()
                    for idx, player in enumerate(players):
                        three_point_field_goals[player] = _normalize_value(threeps[idx])
                if "3PA" in cols:
                    threepsattempted = df["3PA"].tolist()
                    for idx, player in enumerate(players):
                        three_point_field_goals_attempted[player] = _normalize_value(
                            threepsattempted[idx]
                        )
                if "FT" in cols:
                    fts = df["FT"].tolist()
                    for idx, player in enumerate(players):
                        free_throws[player] = _normalize_value(fts[idx])
                if "FTA" in cols:
                    ftas = df["FTA"].tolist()
                    for idx, player in enumerate(players):
                        free_throws_attempted[player] = _normalize_value(ftas[idx])
                if "DRB" in cols:
                    drbs = df["DRB"].tolist()
                    for idx, player in enumerate(players):
                        defensive_rebounds[player] = _normalize_value(drbs[idx])
                if "STL" in cols:
                    stls = df["STL"].tolist()
                    for idx, player in enumerate(players):
                        steals[player] = _normalize_value(stls[idx])
                if "BLK" in cols:
                    blks = df["BLK"].tolist()
                    for idx, player in enumerate(players):
                        blocks[player] = _normalize_value(blks[idx])
                if "PF" in cols:
                    pfs = df["PF"].tolist()
                    for idx, player in enumerate(players):
                        personal_fouls[player] = _normalize_value(pfs[idx])
                if "PTS" in cols:
                    ptss = df["PTS"].tolist()
                    for idx, player in enumerate(players):
                        player_points[player] = _normalize_value(ptss[idx])
                if "GmSc" in cols:
                    gmscs = df["GmSc"].tolist()
                    for idx, player in enumerate(players):
                        game_scores[player] = _normalize_value(gmscs[idx])
                if "+/-" in cols:
                    plusminuses = df["GmSc"].tolist()
                    for idx, player in enumerate(players):
                        point_differentials[player] = _normalize_value(plusminuses[idx])
                if "G" in cols:
                    gs = df["G"].tolist()
                    for idx, player in enumerate(players):
                        goals[player] = _normalize_value(gs[idx])
                if "A" in cols:
                    ass = df["A"].tolist()
                    for idx, player in enumerate(players):
                        assists[player] = _normalize_value(ass[idx])
                if "PIM" in cols:
                    pims = df["PIM"].tolist()
                    for idx, player in enumerate(players):
                        pim = pims[idx]
                        pim_minutes, pim_seconds = pim.split(":")
                        penalties_in_minutes[player] = datetime.timedelta(
                            minutes=int(pim_minutes), seconds=int(pim_seconds)
                        )
                if "EV" in cols:
                    evs = df["EV"].tolist()
                    for idx, player in enumerate(players):
                        even_strength_goals[player] = _normalize_value(evs[idx])
                if "PP" in cols:
                    pps = df["PP"].tolist()
                    for idx, player in enumerate(players):
                        power_play_goals[player] = _normalize_value(pps[idx])
                if "SH" in cols:
                    shs = df["SH"].tolist()
                    for idx, player in enumerate(players):
                        short_handed_goals[player] = _normalize_value(shs[idx])
                if "GW" in cols:
                    gws = df["GW"].tolist()
                    for idx, player in enumerate(players):
                        game_winning_goals[player] = _normalize_value(gws[idx])
                if "S" in cols:
                    ss = df["S"].tolist()
                    for idx, player in enumerate(players):
                        shots_on_goal[player] = _normalize_value(ss[idx])
                if "S%" in cols:
                    sps = df["S%"].tolist()
                    for idx, player in enumerate(players):
                        shooting_percentage[player] = _normalize_value(sps[idx])
                if "SHFT" in cols:
                    shfts = df["SHFT"].tolist()
                    for idx, player in enumerate(players):
                        shifts[player] = _normalize_value(shfts[idx])
                if "TOI" in cols:
                    tois = df["TOI"].tolist()
                    for idx, player in enumerate(players):
                        toi = tois[idx]
                        toi_minutes, toi_seconds = toi.split(":")
                        time_on_ice[player] = datetime.timedelta(
                            minutes=int(toi_minutes), seconds=int(toi_seconds)
                        )
                if "DEC" in cols:
                    decs = df["DEC"].tolist()
                    for idx, player in enumerate(players):
                        decision[player] = _normalize_value(decs[idx])
                if "GA" in cols:
                    gas = df["GA"].tolist()
                    for idx, player in enumerate(players):
                        goals_against[player] = _normalize_value(gas[idx])
                if "SA" in cols:
                    sas = df["SA"].tolist()
                    for idx, player in enumerate(players):
                        shots_against[player] = _normalize_value(sas[idx])
                if "SV" in cols:
                    svs = df["SV"].tolist()
                    for idx, player in enumerate(players):
                        saves[player] = _normalize_value(svs[idx])
                if "SV%" in cols:
                    svps = df["SV%"].tolist()
                    for idx, player in enumerate(players):
                        save_percentage[player] = _normalize_value(svps[idx])
                if "SO" in cols:
                    sos = df["SO"].tolist()
                    for idx, player in enumerate(players):
                        shutouts[player] = _normalize_value(sos[idx])
                if "iCF" in cols:
                    icfs = df["iCF"].tolist()
                    for idx, player in enumerate(players):
                        individual_corsi_for_events[player] = _normalize_value(
                            icfs[idx]
                        )
                if "SAT-F" in cols:
                    satfs = df["SAT-F"].tolist()
                    for idx, player in enumerate(players):
                        on_shot_ice_for_events[player] = _normalize_value(satfs[idx])
                if "SAT-A" in cols:
                    satas = df["SAT-A"].tolist()
                    for idx, player in enumerate(players):
                        on_shot_ice_against_events[player] = _normalize_value(
                            satas[idx]
                        )
                if "CF%" in cols:
                    cfps = df["CF%"].tolist()
                    for idx, player in enumerate(players):
                        corsi_for_percentage[player] = _normalize_value(cfps[idx])
                if "CRel%" in cols:
                    crelps = df["CRel%"].tolist()
                    for idx, player in enumerate(players):
                        relative_corsi_for_percentage[player] = _normalize_value(
                            crelps[idx]
                        )
                if "ZSO" in cols:
                    zsos = df["ZSO"].tolist()
                    for idx, player in enumerate(players):
                        offensive_zone_starts[player] = _normalize_value(zsos[idx])
                if "ZSD" in cols:
                    zsds = df["ZSD"].tolist()
                    for idx, player in enumerate(players):
                        defensive_zone_starts[player] = _normalize_value(zsds[idx])
                if "oZS%" in cols:
                    ozsps = df["oZS%"].tolist()
                    for idx, player in enumerate(players):
                        offensive_zone_start_percentage[player] = _normalize_value(
                            ozsps[idx]
                        )
                if "HIT" in cols:
                    hitss = df["HIT"].tolist()
                    for idx, player in enumerate(players):
                        hits[player] = _normalize_value(hitss[idx])
                if "TS%" in cols:
                    tsps = df["TS%"].tolist()
                    for idx, player in enumerate(players):
                        true_shooting_percentage[player] = _normalize_value(tsps[idx])
                if "AB" in cols:
                    abss = df["AB"].tolist()
                    for idx, player in enumerate(players):
                        at_bats[player] = _normalize_value(abss[idx])
                if "R" in cols:
                    rs = df["R"].tolist()
                    for idx, player in enumerate(players):
                        runs_scored[player] = _normalize_value(rs[idx])
                if "RBI" in cols:
                    rbis = df["RBI"].tolist()
                    for idx, player in enumerate(players):
                        runs_batted_in[player] = _normalize_value(rbis[idx])
                if "BB" in cols:
                    bbs = df["BB"].tolist()
                    for idx, player in enumerate(players):
                        bases_on_balls[player] = _normalize_value(bbs[idx])
                if "SO" in cols:
                    sos = df["SO"].tolist()
                    for idx, player in enumerate(players):
                        strikeouts[player] = _normalize_value(sos[idx])
                if "PA" in cols:
                    pas = df["PA"].tolist()
                    for idx, player in enumerate(players):
                        plate_appearances[player] = _normalize_value(pas[idx])
                if "BA" in cols:
                    bas = df["BA"].tolist()
                    for idx, player in enumerate(players):
                        hits_at_bats[player] = _normalize_value(bas[idx])
                if "OBP" in cols:
                    obps = df["OBP"].tolist()
                    for idx, player in enumerate(players):
                        obp[player] = _normalize_value(obps[idx])
                if "SLG" in cols:
                    slgs = df["SLG"].tolist()
                    for idx, player in enumerate(players):
                        slg[player] = _normalize_value(slgs[idx])
                if "OPS" in cols:
                    opss = df["OPS"].tolist()
                    for idx, player in enumerate(players):
                        ops[player] = _normalize_value(opss[idx])
                if "Pit" in cols:
                    pits = df["Pit"].tolist()
                    for idx, player in enumerate(players):
                        pitches[player] = _normalize_value(pits[idx])
                if "Str" in cols:
                    strs = df["Str"].tolist()
                    for idx, player in enumerate(players):
                        strikes[player] = _normalize_value(strs[idx])
                if "WPA" in cols:
                    wpas = df["WPA"].tolist()
                    for idx, player in enumerate(players):
                        win_probability_added[player] = _normalize_value(wpas[idx])
                if "aLI" in cols:
                    alis = df["aLI"].tolist()
                    for idx, player in enumerate(players):
                        average_leverage_index[player] = _normalize_value(alis[idx])
                if "WPA+" in cols:
                    wpapluss = df["WPA+"].tolist()
                    for idx, player in enumerate(players):
                        wpa_plus[player] = _normalize_value(wpapluss[idx])
                if "WPA-" in cols:
                    wpaminuss = df["WPA-"].tolist()
                    for idx, player in enumerate(players):
                        wpa_minus[player] = _normalize_value(wpaminuss[idx])
                if "cWPA" in cols:
                    cwpas = df["cWPA"].tolist()
                    for idx, player in enumerate(players):
                        cwpa[player] = _normalize_value(cwpas[idx])
                if "acLI" in cols:
                    aclis = df["acLI"].tolist()
                    for idx, player in enumerate(players):
                        acli[player] = _normalize_value(aclis[idx])
                if "RE24" in cols:
                    re24s = df["RE24"].tolist()
                    for idx, player in enumerate(players):
                        re24[player] = _normalize_value(re24s[idx])
                if "PO" in cols:
                    pos = df["PO"].tolist()
                    for idx, player in enumerate(players):
                        putouts[player] = _normalize_value(pos[idx])
                if "IP" in cols:
                    ips = df["IP"].tolist()
                    for idx, player in enumerate(players):
                        innings_pitched[player] = _normalize_value(ips[idx])
                if "ER" in cols:
                    ers = df["ER"].tolist()
                    for idx, player in enumerate(players):
                        earned_runs[player] = _normalize_value(ers[idx])
                if "HR" in cols:
                    hrs = df["HR"].tolist()
                    for idx, player in enumerate(players):
                        home_runs[player] = _normalize_value(hrs[idx])
                if "ERA" in cols:
                    eras = df["ERA"].tolist()
                    for idx, player in enumerate(players):
                        era[player] = _normalize_value(eras[idx])
                if "BF" in cols:
                    bfs = df["BF"].tolist()
                    for idx, player in enumerate(players):
                        batters_faced[player] = _normalize_value(bfs[idx])
                if "Ctct" in cols:
                    ctcts = df["Ctct"].tolist()
                    for idx, player in enumerate(players):
                        strikes_by_contact[player] = _normalize_value(ctcts[idx])
                if "StS" in cols:
                    stss = df["StS"].tolist()
                    for idx, player in enumerate(players):
                        strikes_swinging[player] = _normalize_value(stss[idx])
                if "StL" in cols:
                    stls = df["StL"].tolist()
                    for idx, player in enumerate(players):
                        strikes_looking[player] = _normalize_value(stls[idx])
                if "GB" in cols:
                    gbs = df["GB"].tolist()
                    for idx, player in enumerate(players):
                        ground_balls[player] = _normalize_value(gbs[idx])
                if "FB" in cols:
                    fbs = df["FB"].tolist()
                    for idx, player in enumerate(players):
                        fly_balls[player] = _normalize_value(fbs[idx])
                if "LD" in cols:
                    lds = df["LD"].tolist()
                    for idx, player in enumerate(players):
                        line_drives[player] = _normalize_value(lds[idx])
                if "IR" in cols:
                    irs = df["IR"].tolist()
                    for idx, player in enumerate(players):
                        inherited_runners[player] = _normalize_value(irs[idx])
                if "IS" in cols:
                    iss = df["IS"].tolist()
                    for idx, player in enumerate(players):
                        inherited_scores[player] = _normalize_value(iss[idx])
                if "eFG%" in cols:
                    efgps = df["eFG%"].tolist()
                    for idx, player in enumerate(players):
                        effective_field_goal_percentage[player] = _normalize_value(
                            efgps[idx]
                        )
    except Exception as exc:
        logging.error(url)
        logging.error(response.text)
        logging.error(str(exc))
        return None

    scorebox_meta_div = soup.find("div", class_="scorebox_meta")
    if not isinstance(scorebox_meta_div, Tag):
        dt, teams, venue_name = _find_old_dt(
            dfs=dfs,
            session=session,
            soup=soup,
            url=url,
            league=league,
            player_urls=player_urls,
            fg=fg,
            fga=fga,
            offensive_rebounds=offensive_rebounds,
            assists=assists,
            turnovers=turnovers,
            response=response,
            positions_validator=positions_validator,
            minutes_played=minutes_played,
            three_point_field_goals=three_point_field_goals,
            three_point_field_goals_attempted=three_point_field_goals_attempted,
            free_throws=free_throws,
            free_throws_attempted=free_throws_attempted,
            defensive_rebounds=defensive_rebounds,
            steals=steals,
            blocks=blocks,
            personal_fouls=personal_fouls,
            player_points=player_points,
            game_scores=game_scores,
            point_differentials=point_differentials,
            goals=goals,
            penalties_in_minutes=penalties_in_minutes,
            even_strength_goals=even_strength_goals,
            power_play_goals=power_play_goals,
            short_handed_goals=short_handed_goals,
            game_winning_goals=game_winning_goals,
            even_strength_assists=even_strength_assists,
            power_play_assists=power_play_assists,
            short_handed_assists=short_handed_assists,
            shots_on_goal=shots_on_goal,
            shooting_percentage=shooting_percentage,
            shifts=shifts,
            time_on_ice=time_on_ice,
            decision=decision,
            goals_against=goals_against,
            shots_against=shots_against,
            saves=saves,
            save_percentage=save_percentage,
            shutouts=shutouts,
            individual_corsi_for_events=individual_corsi_for_events,
            on_shot_ice_for_events=on_shot_ice_for_events,
            on_shot_ice_against_events=on_shot_ice_against_events,
            corsi_for_percentage=corsi_for_percentage,
            relative_corsi_for_percentage=relative_corsi_for_percentage,
            offensive_zone_starts=offensive_zone_starts,
            defensive_zone_starts=defensive_zone_starts,
            offensive_zone_start_percentage=offensive_zone_start_percentage,
            hits=hits,
            true_shooting_percentage=true_shooting_percentage,
            at_bats=at_bats,
            runs_scored=runs_scored,
            runs_batted_in=runs_batted_in,
            bases_on_balls=bases_on_balls,
            strikeouts=strikeouts,
            plate_appearances=plate_appearances,
            hits_at_bats=hits_at_bats,
            obp=obp,
            slg=slg,
            ops=ops,
            pitches=pitches,
            strikes=strikes,
            win_probability_added=win_probability_added,
            average_leverage_index=average_leverage_index,
            wpa_plus=wpa_plus,
            wpa_minus=wpa_minus,
            cwpa=cwpa,
            acli=acli,
            re24=re24,
            putouts=putouts,
            innings_pitched=innings_pitched,
            earned_runs=earned_runs,
            home_runs=home_runs,
            era=era,
            batters_faced=batters_faced,
            strikes_by_contact=strikes_by_contact,
            strikes_swinging=strikes_swinging,
            strikes_looking=strikes_looking,
            ground_balls=ground_balls,
            fly_balls=fly_balls,
            line_drives=line_drives,
            inherited_runners=inherited_runners,
            inherited_scores=inherited_scores,
            effective_field_goal_percentage=effective_field_goal_percentage,
        )
    else:
        dt, teams, venue_name = _find_new_dt(
            soup=soup,
            scorebox_meta_div=scorebox_meta_div,
            url=url,
            session=session,
            league=league,
            player_urls=player_urls,
            scores=scores,
            fg=fg,
            fga=fga,
            offensive_rebounds=offensive_rebounds,
            assists=assists,
            turnovers=turnovers,
            positions_validator=positions_validator,
            minutes_played=minutes_played,
            three_point_field_goals=three_point_field_goals,
            three_point_field_goals_attempted=three_point_field_goals_attempted,
            free_throws=free_throws,
            free_throws_attempted=free_throws_attempted,
            defensive_rebounds=defensive_rebounds,
            steals=steals,
            blocks=blocks,
            personal_fouls=personal_fouls,
            player_points=player_points,
            game_scores=game_scores,
            point_differentials=point_differentials,
            goals=goals,
            penalties_in_minutes=penalties_in_minutes,
            even_strength_goals=even_strength_goals,
            power_play_goals=power_play_goals,
            short_handed_goals=short_handed_goals,
            game_winning_goals=game_winning_goals,
            even_strength_assists=even_strength_assists,
            power_play_assists=power_play_assists,
            short_handed_assists=short_handed_assists,
            shots_on_goal=shots_on_goal,
            shooting_percentage=shooting_percentage,
            shifts=shifts,
            time_on_ice=time_on_ice,
            decision=decision,
            goals_against=goals_against,
            shots_against=shots_against,
            saves=saves,
            save_percentage=save_percentage,
            shutouts=shutouts,
            individual_corsi_for_events=individual_corsi_for_events,
            on_shot_ice_for_events=on_shot_ice_for_events,
            on_shot_ice_against_events=on_shot_ice_against_events,
            corsi_for_percentage=corsi_for_percentage,
            relative_corsi_for_percentage=relative_corsi_for_percentage,
            offensive_zone_starts=offensive_zone_starts,
            defensive_zone_starts=defensive_zone_starts,
            offensive_zone_start_percentage=offensive_zone_start_percentage,
            hits=hits,
            true_shooting_percentage=true_shooting_percentage,
            at_bats=at_bats,
            runs_scored=runs_scored,
            runs_batted_in=runs_batted_in,
            bases_on_balls=bases_on_balls,
            strikeouts=strikeouts,
            plate_appearances=plate_appearances,
            hits_at_bats=hits_at_bats,
            obp=obp,
            slg=slg,
            ops=ops,
            pitches=pitches,
            strikes=strikes,
            win_probability_added=win_probability_added,
            average_leverage_index=average_leverage_index,
            wpa_plus=wpa_plus,
            wpa_minus=wpa_minus,
            cwpa=cwpa,
            acli=acli,
            re24=re24,
            putouts=putouts,
            innings_pitched=innings_pitched,
            earned_runs=earned_runs,
            home_runs=home_runs,
            era=era,
            batters_faced=batters_faced,
            strikes_by_contact=strikes_by_contact,
            strikes_swinging=strikes_swinging,
            strikes_looking=strikes_looking,
            ground_balls=ground_balls,
            fly_balls=fly_balls,
            line_drives=line_drives,
            inherited_runners=inherited_runners,
            inherited_scores=inherited_scores,
            effective_field_goal_percentage=effective_field_goal_percentage,
        )
    for team in teams:
        if team.name == "File Not Found":
            raise ValueError("team name is File Not Found (invalid)")

    season_type = SeasonType.REGULAR
    for h2 in soup.find_all("h2"):
        a = h2.find("a")
        if a is None:
            continue
        season_text = a.get_text().strip()
        match season_text:
            case "Big Sky Conference":
                season_type = SeasonType.REGULAR
            case "Big East Conference":
                season_type = SeasonType.REGULAR
            case "Big West Conference":
                season_type = SeasonType.REGULAR
            case "Big Ten Conference":
                season_type = SeasonType.REGULAR
            case "Mid-American Conference":
                season_type = SeasonType.REGULAR
            case "Horizon League":
                season_type = SeasonType.REGULAR
            case "Atlantic 10 Conference":
                season_type = SeasonType.REGULAR
            case "Mountain West Conference":
                season_type = SeasonType.REGULAR
            case "West Coast Conference":
                season_type = SeasonType.REGULAR
            case "American Athletic Conference":
                season_type = SeasonType.REGULAR
            case "Coastal Athletic Association":
                season_type = SeasonType.REGULAR
            case "Conference USA":
                season_type = SeasonType.REGULAR
            case "America East Conference":
                season_type = SeasonType.REGULAR
            case "Sun Belt Conference":
                season_type = SeasonType.REGULAR
            case "Metro Atlantic Athletic Conference":
                season_type = SeasonType.REGULAR
            case "Atlantic Sun Conference":
                season_type = SeasonType.REGULAR
            case "Ohio Valley Conference":
                season_type = SeasonType.REGULAR
            case "Mid-Eastern Athletic Conference":
                season_type = SeasonType.REGULAR
            case "Big South Conference":
                season_type = SeasonType.REGULAR
            case "Summit League":
                season_type = SeasonType.REGULAR
            case "Western Athletic Conference":
                season_type = SeasonType.REGULAR
            case "Big 12 Conference":
                season_type = SeasonType.REGULAR
            case "Southeastern Conference":
                season_type = SeasonType.REGULAR
            case "Patriot League":
                season_type = SeasonType.REGULAR
            case "Southern Conference":
                season_type = SeasonType.REGULAR
            case "Missouri Valley Conference":
                season_type = SeasonType.REGULAR
            case "Atlantic Coast Conference":
                season_type = SeasonType.REGULAR
            case "Southwest Athletic Conference":
                season_type = SeasonType.REGULAR
            case "Southland Conference":
                season_type = SeasonType.REGULAR
            case "Northeast Conference":
                season_type = SeasonType.REGULAR
            case "Ivy League":
                season_type = SeasonType.REGULAR
            case "NCAA Men's Tournament":
                season_type = SeasonType.REGULAR
            case "Pac-12 Conference":
                season_type = SeasonType.REGULAR
            case "Colonial Athletic Association":
                season_type = SeasonType.REGULAR
            case "Pacific-12 Conference":
                season_type = SeasonType.REGULAR
            case "NCAA Women's Tournament":
                season_type = SeasonType.REGULAR
            case "Pacific-10 Conference":
                season_type = SeasonType.REGULAR
            case "Great West Conference":
                season_type = SeasonType.REGULAR
            case _:
                logging.warning("Unrecognised Season Text: %s", season_text)
        break

    game_text = soup.get_text().replace("\n", "")
    attendance = None
    if "Attendance:" in game_text:
        attendance = int(
            game_text.split("Attendance:")[1]
            .strip()
            .split()[0]
            .strip()
            .replace(",", "")
            .replace("Time", "")
            .replace("Show/Hide", "")
            .replace("Team", "")
            .replace("Arena:", "")
            .replace("Copyright", "")
            .replace("Venue:", "")
        )

    try:
        return GameModel(
            dt=dt,
            week=None,
            game_number=None,
            venue=create_sportsreference_venue_model(venue_name, session, dt),  # pyright: ignore
            teams=teams,
            league=str(league),
            year=dt.year,
            season_type=season_type,
            end_dt=None,
            attendance=attendance,
            postponed=None,
            play_off=None,
            distance=None,
            dividends=[],
            pot=None,
            version=version,
        )
    except ValueError as exc:
        logging.error(response.text)
        logging.error(url)
        raise exc


@MEMORY.cache(ignore=["session"])
def _cached_create_sportsreference_game_model(
    session: ScrapeSession,
    url: str,
    league: League,
    positions_validator: dict[str, str],
    version: str,
) -> GameModel | None:
    return _create_sportsreference_game_model(
        session=session,
        url=url,
        league=league,
        positions_validator=positions_validator,
        version=version,
    )


def create_sportsreference_game_model(
    session: ScrapeSession,
    url: str,
    league: League,
    positions_validator: dict[str, str],
) -> GameModel | None:
    """Create a sports reference game model."""
    if not pytest_is_running.is_running():
        return _cached_create_sportsreference_game_model(
            session=session,
            url=url,
            league=league,
            positions_validator=positions_validator,
            version=VERSION,
        )
    with session.cache_disabled():
        return _create_sportsreference_game_model(
            session=session,
            url=url,
            league=league,
            positions_validator=positions_validator,
            version=VERSION,
        )
