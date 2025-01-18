"""NFL SportsDB team model."""

# pylint: disable=too-many-arguments
import datetime

import requests

from ....cache import MEMORY
from ...google.google_news_model import create_google_news_models
from ...league import League
from ...team_model import TeamModel


@MEMORY.cache(ignore=["session"])
def create_nfl_sportsdb_team_model(
    team_id: str,
    name: str,
    points: float,
    session: requests.Session,
    dt: datetime.datetime,
    league: League,
) -> TeamModel:
    """Create a team model based off the sportsdb NFL response."""
    return TeamModel(
        identifier=team_id,
        name=name,
        points=points,
        players=[],
        odds=[],
        ladder_rank=None,
        location=None,
        news=create_google_news_models(name, session, dt, league),
    )
