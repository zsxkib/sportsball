"""Combined season model."""

from typing import Iterator, Type

import requests

from ..game_model import GameModel
from ..season_model import SeasonModel
from ..season_type import SeasonType
from .combined_game_model import CombinedGameModel


class CombinedSeasonModel(SeasonModel):
    """The class implementing the combined season model."""

    def __init__(
        self, session: requests.Session, season_models: list[SeasonModel]
    ) -> None:
        super().__init__(session)
        self._season_models = season_models

    @classmethod
    def combined_game_model_class(cls) -> Type[CombinedGameModel]:
        """The class representing a combined game model."""
        return CombinedGameModel

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
        game_model_class = self.combined_game_model_class()
        team_model_class = game_model_class.combined_team_model_class()
        team_identity_map = team_model_class.team_identity_map()
        for season_model in self._season_models:
            for game_model in season_model.games:
                game_components = [str(game_model.dt.date())]
                for team in game_model.teams:
                    team_identifier = team_identity_map[team.identifier]
                    game_components.append(team_identifier)
                game_components = sorted(game_components)
                key = "-".join(game_components)
                games[key] = games.get(key, []) + [game_model]
        for game_models in games.values():
            yield game_model_class(self.session, game_models)
