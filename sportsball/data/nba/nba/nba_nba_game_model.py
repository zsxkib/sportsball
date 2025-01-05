"""NBA NBA API game model."""

import pandas as pd
import pytz
from dateutil.parser import parse

from ....cache import MEMORY
from ...game_model import GameModel
from ...league import League
from ...season_type import SeasonType
from .nba_nba_team_model import create_nba_nba_team_model

_SEASON_TYPE_MAP = {
    "1": SeasonType.PRESEASON,
    "2": SeasonType.REGULAR,
    "3": SeasonType.OFFSEASON,
    "4": SeasonType.POSTSEASON,
    "5": SeasonType.POSTSEASON,
    "6": SeasonType.OFFSEASON,
}


@MEMORY.cache
def create_nba_nba_game_model(
    row: pd.Series,
    league: League,
    week: int,
    game_number: int,
) -> GameModel:
    """Create a game model from NBA API."""
    season_id = row["SEASON_ID"]
    dt = pytz.timezone("EST").localize(parse(row["GAME_DATE"]))
    return GameModel(
        dt=dt,
        week=week,
        game_number=game_number,
        venue=None,
        teams=[
            x
            for x in [
                create_nba_nba_team_model(row, True),  # type: ignore
                create_nba_nba_team_model(row, False),  # type: ignore
            ]
            if x is not None
        ],
        end_dt=None,
        attendance=None,
        league=league,
        year=int(season_id[1:]),
        season_type=_SEASON_TYPE_MAP[season_id[0]],
    )
