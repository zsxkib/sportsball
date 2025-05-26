"""HKJC HKJC game model."""

import datetime
from typing import Any

import pytest_is_running
import requests_cache

from ....cache import MEMORY
from ...game_model import GameModel
from ...league import League
from .hkjc_hkjc_team_model import create_hkjc_hkjc_team_model
from .hkjc_hkjc_venue_model import create_hkjc_hkjc_venue_model

POST_TIME_KEY = "postTime"
RACE_RESULTS_KEY = "raceResults"
RACE_TIME_KEY = "raceTime"
DISTANCE_KEY = "distance"
RACE_NUMBER_KEY = "no"
COUNTRY_KEY = "country_en"
RACE_TRACK_KEY = "raceTrack"
DESCRIPTION_KEY = "description_en"
RACE_COURSE_KEY = "raceCourse"
RUNNERS_KEY = "runners"


def _create_hkjc_hkjc_game_model(
    session: requests_cache.CachedSession,
    race: dict[str, Any],
    league: League,
    venue_code: str,
) -> GameModel:
    dt = datetime.datetime.fromisoformat(race[POST_TIME_KEY])
    end_t = datetime.datetime.strptime(race[RACE_RESULTS_KEY][0][RACE_TIME_KEY], "%M:%S.%f")
    end_dt = dt + datetime.timedelta(
        minutes=end_t.minute, seconds=end_t.second, milliseconds=end_t.microsecond
    )
    distance = race[DISTANCE_KEY]
    print(race)
    return GameModel(
        dt=dt,
        week=None,
        game_number=race[RACE_NUMBER_KEY],
        venue=create_hkjc_hkjc_venue_model(
            session,
            dt,
            race[COUNTRY_KEY],
            race[RACE_TRACK_KEY][DESCRIPTION_KEY].lower(),
            race[RACE_COURSE_KEY][DESCRIPTION_KEY],
            venue_code=venue_code,
        ),
        teams=[
            create_hkjc_hkjc_team_model(x, len(race[RUNNERS_KEY]))
            for x in race[RUNNERS_KEY]
        ],
        end_dt=end_dt,
        attendance=None,
        league=str(league),
        year=dt.year,
        season_type=None,
        postponed=None,
        play_off=None,
        distance=distance,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_hkjc_hkjc_game_model(
    session: requests_cache.CachedSession,
    race: dict[str, Any],
    league: League,
    venue_code: str,
) -> GameModel:
    """Create a game model from NBA API."""
    return _create_hkjc_hkjc_game_model(session, race, league, venue_code)


def create_hkjc_hkjc_game_model(
    session: requests_cache.CachedSession,
    race: dict[str, Any],
    league: League,
    venue_code: str,
) -> GameModel:
    """Create a game model from NBA API."""
    if not pytest_is_running.is_running():
        return _cached_create_hkjc_hkjc_game_model(session, race, league, venue_code)
    with session.cache_disabled():
        return _cached_create_hkjc_hkjc_game_model(session, race, league, venue_code)
