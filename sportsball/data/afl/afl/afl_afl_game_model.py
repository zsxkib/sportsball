"""AFL AFL game model."""

# pylint: disable=too-many-statements,protected-access,too-many-arguments
import datetime

import requests_cache

from ...game_model import GameModel
from ...league import League
from .afl_afl_team_model import create_afl_afl_team_model
from .afl_afl_venue_model import create_afl_afl_venue_model


def create_afl_afl_game_model(
    team_names: list[str],
    players: list[list[tuple[str, str, str, str]]],
    dt: datetime.datetime,
    venue_name: str,
    session: requests_cache.CachedSession,
    ladder: list[str],
) -> GameModel:
    """Create a game model from AFL Tables."""
    venue_model = create_afl_afl_venue_model(venue_name, session, dt)
    teams = [
        create_afl_afl_team_model(x, players[count], session, dt, ladder)
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
