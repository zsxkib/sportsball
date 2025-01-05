"""NBA API player model."""

import json

import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo  # type: ignore

from ....cache import MEMORY
from ...player_model import PlayerModel


@MEMORY.cache
def create_nba_nba_player_model(
    row: pd.Series, player_index: pd.DataFrame
) -> PlayerModel:
    """Create a player model from NBA API."""
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
    return PlayerModel(identifier=player_id, jersey=jersey, kicks=None, fumbles=None)
