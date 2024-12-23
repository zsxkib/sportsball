"""NFL combined season model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Type, Union

from ...combined.combined_game_model import CombinedGameModel
from ...combined.combined_season_model import CombinedSeasonModel
from ..espn.nfl_espn_season_model import NFLESPNSeasonModel
from ..sportsdb.nfl_sportsdb_season_model import NFLSportsDBSeasonModel
from .nfl_combined_game_model import NFLCombinedGameModel


class NFLCombinedSeasonModel(CombinedSeasonModel):
    """The class implementing the NFL combined season model."""

    @classmethod
    def _combined_game_model_class(cls) -> Type[CombinedGameModel]:
        return NFLCombinedGameModel

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **NFLSportsDBSeasonModel.urls_expire_after(),
            **NFLESPNSeasonModel.urls_expire_after(),
            **NFLCombinedGameModel.urls_expire_after(),
        }
