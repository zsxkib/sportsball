"""ESPN player model."""

from typing import Any

import requests

from ...cache import MEMORY
from ..player_model import PlayerModel


@MEMORY.cache(ignore=["session"])
def create_espn_player_model(
    session: requests.Session, player: dict[str, Any]
) -> PlayerModel:
    """Create a player model based off ESPN."""
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
    )
