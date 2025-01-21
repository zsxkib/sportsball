"""NCAAB Sports Reference game model."""

# pylint: disable=too-many-locals,too-many-statements
import logging
import urllib.parse

import requests
from bs4 import BeautifulSoup, Tag
from dateutil.parser import parse

from ....cache import MEMORY
from ...game_model import GameModel
from ...league import League
from ...season_type import SeasonType
from ...team_model import TeamModel
from .ncaab_sportsreference_team_model import \
    create_ncaab_sportsreference_team_model
from .ncaab_sportsreference_venue_model import \
    create_ncaab_sportsreference_venue_model


@MEMORY.cache(ignore=["session"])
def create_ncaab_sportsreference_game_model(
    session: requests.Session,
    url: str,
    league: League,
) -> GameModel:
    """Create an NCAAB sports reference game model."""
    # print(f"Game URL: {url}")
    response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    scorebox_meta_div = soup.find("div", class_="scorebox_meta")
    if not isinstance(scorebox_meta_div, Tag):
        raise ValueError("scorebox_meta_div is not a Tag.")

    in_divs = scorebox_meta_div.find_all("div")
    in_div = in_divs[0]
    in_div_text = in_div.get_text().strip()
    dt = parse(in_div_text)
    venue_div = in_divs[1]
    venue_name = venue_div.get_text().strip()
    scorebox_div = soup.find("div", class_="scorebox")
    if not isinstance(scorebox_div, Tag):
        raise ValueError("scorebox_div is not a Tag.")

    player_urls = set()
    for a in soup.find_all("a"):
        player_url = urllib.parse.urljoin(url, a.get("href"))
        if "/players/" in player_url and not player_url.endswith("/players/"):
            player_urls.add(player_url)

    scores = []
    for score_div in soup.find_all("div", class_="score"):
        scores.append(float(score_div.get_text().strip()))

    teams: list[TeamModel] = []
    for a in scorebox_div.find_all("a"):
        team_url = urllib.parse.urljoin(url, a.get("href"))
        if "/schools/" in team_url:
            teams.append(
                create_ncaab_sportsreference_team_model(
                    session, team_url, dt, league, player_urls, scores[len(teams)]
                )
            )

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
            case _:
                logging.warning("Unrecognised Season Text: %s", season_text)
        break

    return GameModel(
        dt=dt,
        week=None,
        game_number=None,
        venue=create_ncaab_sportsreference_venue_model(venue_name, session, dt),  # pyright: ignore
        teams=teams,
        league=league,
        year=dt.year,
        season_type=season_type,
        end_dt=None,
        attendance=None,
    )
