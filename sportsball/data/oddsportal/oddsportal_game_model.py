"""OddsPortal game model."""

# pylint: disable=too-many-locals
import datetime
import json
import urllib.parse

import pytest_is_running
import requests_cache
from bs4 import BeautifulSoup, Tag

from ...cache import MEMORY
from ..game_model import GameModel
from ..league import League
from .oddsportal_team_model import create_oddsportal_team_model
from .oddsportal_venue_model import create_oddsportal_venue_model


def _create_oddsportal_game_model(
    session: requests_cache.CachedSession,
    url: str,
    league: League,
) -> GameModel:
    response = session.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    event_tag = soup.find("div", id="react-event-header")
    if not isinstance(event_tag, Tag):
        raise ValueError(f"event_tag is not a tag for URL: {url}.")
    event = json.loads(str(event_tag["data"]))

    event_body = event["eventBody"]
    event_data = event["eventData"]
    dt = datetime.datetime.fromtimestamp(event_body["startDate"])
    end_dt = None
    if event_body.get("endDate", False) is not False:
        end_dt = datetime.datetime.fromtimestamp(event_body["endDate"])
    version_id = str(event_data["versionId"])
    sport_id = str(event_data["sportId"])
    unique_id = event_data["id"]
    default_bet_id = str(event_data["defaultBetId"])
    default_scope_id = str(event_data["defaultScopeId"])
    xhash = urllib.parse.unquote(event_data["xhash"])

    salt: bytes | None = None
    password: bytes | None = None
    for script in soup.find_all("script"):
        src = script.get("src")
        if src is None:
            continue
        if "/app.js" in src:
            src_url = urllib.parse.urljoin(url, src)
            src_response = session.get(src_url)
            src_response.raise_for_status()
            variables = src_response.text
            sentinel = 'break}return e.next=9,g(r.data,"'
            variables = variables[variables.find(sentinel) + len(sentinel) :]
            variables = variables[
                : variables.find('");case 9:return s=e.sent,l=JSON.parse(s),e.abrupt')
            ]
            password_str, salt_str = variables.split('","')
            salt = str.encode(salt_str)
            password = str.encode(password_str)
            break
    if salt is None:
        raise ValueError("salt is null.")
    if password is None:
        raise ValueError("password is null.")

    bookie_names = event_body["providersNames"]
    home_points = None
    if event_body["homeResult"] != "":
        home_points = float(event_body["homeResult"])
    away_points = None
    if event_body["awayResult"] != "":
        away_points = float(event_body["awayResult"])

    return GameModel(
        dt=dt,
        week=None,
        game_number=None,
        venue=create_oddsportal_venue_model(
            session,
            dt,
            event_body["venue"],
            event_body["venueTown"],
            event_body["venueCountry"],
        ),
        teams=[
            create_oddsportal_team_model(
                session,
                dt,
                event_data["home"],
                league,
                home_points,
                version_id,
                sport_id,
                unique_id,
                default_bet_id,
                default_scope_id,
                xhash,
                salt,
                password,
                bookie_names,
                0,
            ),
            create_oddsportal_team_model(
                session,
                dt,
                event_data["away"],
                league,
                away_points,
                version_id,
                sport_id,
                unique_id,
                default_bet_id,
                default_scope_id,
                xhash,
                salt,
                password,
                bookie_names,
                1,
            ),
        ],
        end_dt=end_dt,
        attendance=None,
        league=league,
        year=dt.year,
        season_type=None,
        postponed=event_data["isPostponed"],
        play_off=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_oddsportal_game_model(
    session: requests_cache.CachedSession,
    url: str,
    league: League,
) -> GameModel:
    return _create_oddsportal_game_model(session, url, league)


def create_oddsportal_game_model(
    session: requests_cache.CachedSession,
    url: str,
    league: League,
    is_next: bool,
) -> GameModel:
    """Create a OddsPortal game model."""
    if not pytest_is_running.is_running() and not is_next:
        return _cached_create_oddsportal_game_model(session, url, league)
    with session.cache_disabled():
        return _create_oddsportal_game_model(session, url, league)
