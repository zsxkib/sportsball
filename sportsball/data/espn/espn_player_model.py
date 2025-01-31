"""ESPN player model."""

# pylint: disable=duplicate-code
import datetime
from typing import Any

import pytest_is_running
import requests_cache

from ...cache import MEMORY
from ..player_model import PlayerModel


def _create_espn_player_model(
    session: requests_cache.CachedSession, player: dict[str, Any]
) -> PlayerModel:
    identifier = str(player["playerId"])
    jersey = player.get("jersey")
    fumbles = None
    fumbles_lost = None
    if "statistics" in player:
        statistics_response = session.get(player["statistics"]["$ref"])
        if statistics_response.ok:
            statistics_dict = statistics_response.json()
            fumbles = None
            for category in statistics_dict["splits"]["categories"]:
                for stat in category["stats"]:
                    if stat["name"] == "fumbles":
                        fumbles = stat["value"]
                    if stat["name"] == "fumblesLost":
                        fumbles_lost = stat["value"]
    return PlayerModel(
        identifier=identifier,
        jersey=jersey,
        kicks=None,
        fumbles=fumbles,
        fumbles_lost=fumbles_lost,
        field_goals=None,
        field_goals_attempted=None,
        offensive_rebounds=None,
        assists=None,
        turnovers=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_espn_player_model(
    session: requests_cache.CachedSession, player: dict[str, Any]
) -> PlayerModel:
    return _create_espn_player_model(session, player)


def create_espn_player_model(
    session: requests_cache.CachedSession, player: dict[str, Any], dt: datetime.datetime
) -> PlayerModel:
    """Create a player model based off ESPN."""
    if (
        not pytest_is_running.is_running()
        and dt < datetime.datetime.now() - datetime.timedelta(days=7)
    ):
        return _cached_create_espn_player_model(session, player)
    with session.cache_disabled():
        return _create_espn_player_model(session, player)
