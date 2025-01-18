"""ESPN team model."""

# pylint: disable=too-many-arguments

import datetime
from typing import Any

import requests

from ...cache import MEMORY
from ..google.google_news_model import create_google_news_models
from ..league import League
from ..odds_model import OddsModel
from ..team_model import TeamModel
from .espn_player_model import create_espn_player_model


@MEMORY.cache(ignore=["session"])
def create_espn_team_model(
    session: requests.Session,
    team: dict[str, Any],
    roster_dict: dict[str, Any],
    odds: list[OddsModel],
    score_dict: dict[str, Any],
    dt: datetime.datetime,
    league: League,
) -> TeamModel:
    """Create team model from ESPN."""
    identifier = team["id"]
    name = team.get("name", team.get("fullName", team.get("displayName")))
    if name is None:
        raise ValueError("name is null")
    location = team["location"]
    players = []
    for entity in roster_dict.get("entries", []):
        player = create_espn_player_model(session, entity)
        players.append(player)
    points = score_dict["value"]
    return TeamModel(
        identifier=identifier,
        name=name,
        location=location,
        players=players,
        odds=odds,
        points=points,
        ladder_rank=None,
        news=create_google_news_models(name, session, dt, league),
    )
