"""NFL combined game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Type, Union

from ...combined.combined_game_model import CombinedGameModel
from ...combined.combined_team_model import CombinedTeamModel
from ...combined.combined_venue_model import CombinedVenueModel
from ..espn.nfl_espn_game_model import NFLESPNGameModel
from ..sportsdb.nfl_sportsdb_game_model import NFLSportsDBGameModel
from .nfl_combined_team_model import NFLCombinedTeamModel
from .nfl_combined_venue_model import NFLCombinedVenueModel


class NFLCombinedGameModel(CombinedGameModel):
    """NFL combined implementation of the game model."""

    # pylint: disable=abstract-method

    @classmethod
    def _combined_team_model_class(cls) -> Type[CombinedTeamModel]:
        return NFLCombinedTeamModel

    @classmethod
    def _combined_venue_model_class(cls) -> Type[CombinedVenueModel]:
        return NFLCombinedVenueModel

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **NFLSportsDBGameModel.urls_expire_after(),
            **NFLESPNGameModel.urls_expire_after(),
            **NFLCombinedTeamModel.urls_expire_after(),
            **NFLCombinedVenueModel.urls_expire_after(),
        }
