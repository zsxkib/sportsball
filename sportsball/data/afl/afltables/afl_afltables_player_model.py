"""AFL AFLTables player model."""

# pylint: disable=line-too-long
import datetime
import os
from urllib.parse import urlparse

import pytest_is_running
import requests_cache

from ....cache import MEMORY
from ...player_model import PlayerModel


def _create_afl_afltables_player_model(
    player_url: str, jersey: str, kicks: int | None
) -> PlayerModel:
    o = urlparse(player_url)
    last_component = o.path.split("/")[-1]
    identifier, _ = os.path.splitext(last_component)
    jersey = "".join(filter(str.isdigit, jersey))
    return PlayerModel(
        identifier=identifier,
        jersey=jersey,
        kicks=kicks,
        fumbles=None,
        fumbles_lost=None,
        field_goals=None,
        field_goals_attempted=None,
        offensive_rebounds=None,
        assists=None,
        turnovers=None,
    )


@MEMORY.cache
def _cached_create_afl_afltables_player_model(
    player_url: str, jersey: str, kicks: int | None
) -> PlayerModel:
    return _create_afl_afltables_player_model(player_url, jersey, kicks)


def create_afl_afltables_player_model(
    player_url: str,
    jersey: str,
    kicks: int | None,
    dt: datetime.datetime,
    session: requests_cache.CachedSession,
) -> PlayerModel:
    """Create a player model from AFL Tables."""
    if (
        not pytest_is_running.is_running()
        and dt < datetime.datetime.now() - datetime.timedelta(days=7)
    ):
        return _cached_create_afl_afltables_player_model(player_url, jersey, kicks)  # pyright: ignore
    with session.cache_disabled():
        return _create_afl_afltables_player_model(player_url, jersey, kicks)
