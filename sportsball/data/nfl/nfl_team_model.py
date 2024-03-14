"""NFL team model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ..odds_model import OddsModel
from ..team_model import TeamModel
from .nfl_odds_model import NFLOddsModel
from .nfl_player_model import NFLPlayerModel


class NFLTeamModel(TeamModel):
    """NFL implementation of the team model."""

    def __init__(
        self,
        team: Dict[str, Any],
        roster_dict: Dict[str, Any],
        odds: Dict[str, OddsModel],
    ) -> None:
        identifier = team["id"]

        name = team.get("name", team.get("fullName", team.get("displayName")))
        if name is None:
            raise ValueError("name is null")

        location = team["location"]
        players = []
        for entity in roster_dict.get("entries", []):
            player = NFLPlayerModel(entity)
            players.append(player)
        super().__init__(identifier, name, location, players, odds)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **NFLPlayerModel.urls_expire_after(),
            **NFLOddsModel.urls_expire_after(),
        }
