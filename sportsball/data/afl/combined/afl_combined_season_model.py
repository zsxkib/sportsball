"""AFL combined season model."""

# pylint: disable=line-too-long
import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests_cache

from ...game_model import GameModel
from ...season_model import SeasonModel
from ...season_type import SeasonType
from ..afltables.afl_afltables_season_model import AFLAFLTablesSeasonModel
from .afl_combined_game_model import AFLCombinedGameModel


class AFLCombinedSeasonModel(SeasonModel):
    """The class implementing the AFL combined season model."""

    def __init__(
        self, session: requests_cache.CachedSession, season_model: SeasonModel
    ) -> None:
        super().__init__(session)
        self._season_model = season_model

    @property
    def year(self) -> int | None:
        """Return the year."""
        return self._season_model.year

    @property
    def season_type(self) -> SeasonType | None:
        """Return the season type."""
        return self._season_model.season_type

    @property
    def games(self) -> Iterator[GameModel]:
        for game_model in self._season_model.games:
            yield AFLCombinedGameModel(self.session, game_model)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **AFLAFLTablesSeasonModel.urls_expire_after(),
            **AFLCombinedGameModel.urls_expire_after(),
        }
