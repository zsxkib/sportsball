"""NFL SportsDB game model."""

# pylint: disable=too-many-arguments
import datetime
from typing import Any

import requests
from dateutil import parser

from ....cache import MEMORY
from ...game_model import GameModel
from ...league import League
from ...season_type import SeasonType
from .nfl_sportsdb_team_model import create_nfl_sportsdb_team_model
from .nfl_sportsdb_venue_model import create_nfl_sportsdb_venue_model


@MEMORY.cache(ignore=["session"])
def create_nfl_sportsdb_game_model(
    session: requests.Session,
    game: dict[str, Any],
    week_number: int,
    game_number: int,
    league: League,
    year: int | None,
    season_type: SeasonType | None,
) -> GameModel:
    """Create an NFL SportsDB game model."""
    try:
        dt = datetime.datetime.fromisoformat(game["strTimestamp"])
    except TypeError:
        dt = parser.parse(game["dateEvent"])
    venue = create_nfl_sportsdb_venue_model(session, game["idVenue"], dt)
    home_score = float(game["intHomeScore"] if game["intHomeScore"] is not None else 0)
    away_score = float(game["intAwayScore"] if game["intAwayScore"] is not None else 0)
    teams = [
        create_nfl_sportsdb_team_model(
            game["idHomeTeam"],
            game["strHomeTeam"],
            home_score,
            session,
            dt,
            league,
        ),
        create_nfl_sportsdb_team_model(
            game["idAwayTeam"],
            game["strAwayTeam"],
            away_score,
            session,
            dt,
            league,
        ),
    ]
    return GameModel(
        dt=dt,
        week=week_number,
        game_number=game_number,
        venue=venue,  # pyright: ignore
        teams=teams,  # pyright: ignore
        league=league,
        year=year,
        season_type=season_type,
        end_dt=None,
        attendance=None,
    )
