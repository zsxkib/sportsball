"""AFL AFLTables player model."""

import os
from urllib.parse import urlparse

from ....cache import MEMORY
from ...player_model import PlayerModel


@MEMORY.cache
def create_afl_afltables_player_model(
    player_url: str, jersey: str, kicks: int | None
) -> PlayerModel:
    """Create a player model from AFL Tables."""
    o = urlparse(player_url)
    last_component = o.path.split("/")[-1]
    identifier, _ = os.path.splitext(last_component)
    jersey = "".join(filter(str.isdigit, jersey))
    return PlayerModel(identifier=identifier, jersey=jersey, kicks=kicks, fumbles=None)
