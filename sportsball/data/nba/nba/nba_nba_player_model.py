"""NBA API player model."""

# pylint: disable=duplicate-code
import datetime
import json

import pandas as pd
import pytest_is_running
import requests_cache
from nba_api.stats.endpoints import commonplayerinfo  # type: ignore

from ....cache import MEMORY
from ...player_model import PlayerModel


def _create_nba_nba_player_model(
    row: pd.Series, player_index: pd.DataFrame
) -> PlayerModel:
    jersey = None
    player_id = str(row["PERSON_ID"])
    player_index_df = player_index[player_index["PERSON_ID"].astype(str) == player_id]
    if not player_index_df.empty:
        jersey = player_index_df.iloc[0]["JERSEY_NUMBER"]
    else:
        try:
            cpi = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
            cpi_row = cpi.common_player_info.get_data_frame().squeeze(axis=0)
            jersey = cpi_row["JERSEY"]
        except json.decoder.JSONDecodeError:
            pass
    return PlayerModel(
        identifier=player_id,
        jersey=jersey,
        kicks=None,
        fumbles=None,
        fumbles_lost=None,
        field_goals=None,
        field_goals_attempted=None,
        offensive_rebounds=None,
        assists=None,
        turnovers=None,
    )


@MEMORY.cache
def _cached_create_nba_nba_player_model(
    row: pd.Series, player_index: pd.DataFrame
) -> PlayerModel:
    return _create_nba_nba_player_model(row, player_index)


def create_nba_nba_player_model(
    row: pd.Series,
    player_index: pd.DataFrame,
    dt: datetime.datetime,
    session: requests_cache.CachedSession,
) -> PlayerModel:
    """Create a player model from NBA API."""
    if not pytest_is_running.is_running() and dt < datetime.datetime.now().replace(
        tzinfo=dt.tzinfo
    ) - datetime.timedelta(days=7):
        return _cached_create_nba_nba_player_model(row, player_index)  # pyright: ignore
    with session.cache_disabled():
        return _create_nba_nba_player_model(row, player_index)
