"""ESPN player model."""

from typing import Any

from ...cache import MEMORY
from ..player_model import PlayerModel


@MEMORY.cache
def create_espn_player_model(player: dict[str, Any]) -> PlayerModel:
    """Create a player model based off ESPN."""
    identifier = str(player["playerId"])
    jersey = player.get("jersey")
    return PlayerModel(identifier=identifier, jersey=jersey, kicks=None)
