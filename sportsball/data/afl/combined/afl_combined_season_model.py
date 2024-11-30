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
        self, session: requests_cache.CachedSession, season_models: list[SeasonModel]
    ) -> None:
        super().__init__(session)
        self._season_models = season_models

    @property
    def year(self) -> int | None:
        """Return the year."""
        year = None
        for season_model in self._season_models:
            year = season_model.year
            if year:
                break
        return year

    @property
    def season_type(self) -> SeasonType | None:
        """Return the season type."""
        season_type = None
        for season_model in self._season_models:
            season_type = season_model.season_type
            if season_type:
                break
        return season_type

    @property
    def games(self) -> Iterator[GameModel]:
        games: dict[str, list[GameModel]] = {}
        for season_model in self._season_models:
            for game_model in season_model.games:
                game_components = [str(game_model.dt.date())]
                for team in game_model.teams:
                    game_components.append(team.name)
                game_components = sorted(game_components)
                key = "-".join(game_components)
                games[key] = games.get(key, []) + [game_model]
        for game_models in games.values():
            yield AFLCombinedGameModel(self.session, game_models)

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
