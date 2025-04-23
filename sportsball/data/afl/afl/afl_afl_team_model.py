"""AFL AFL team model."""

# pylint: disable=duplicate-code
import datetime

import requests_cache

from ...google.google_news_model import create_google_news_models
from ...league import League
from ...team_model import TeamModel
from .afl_afl_player_model import create_afl_afl_player_model


def create_afl_afl_team_model(
    team_name: str,
    players: list[tuple[str, str, str, str]],
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
    ladder: list[str],
) -> TeamModel:
    """Create a team model from AFL AFL."""
    player_models = [
        create_afl_afl_player_model(
            identifier, player_number, " ".join([first_name, second_name])
        )
        for identifier, player_number, first_name, second_name in players
    ]
    return TeamModel(
        identifier=team_name,
        name=team_name,
        location=None,
        players=player_models,
        odds=[],
        points=None,
        ladder_rank=ladder.index(team_name) + 1,
        kicks=None,
        news=create_google_news_models(team_name, session, dt, League.AFL),
        social=[],
        field_goals=None,
        field_goals_attempted=None,
        offensive_rebounds=None,
        assists=None,
        turnovers=None,
    )
