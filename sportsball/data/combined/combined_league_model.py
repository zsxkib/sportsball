"""Combined league model."""

import logging
from typing import Iterator

import requests
import tqdm

from ..game_model import GameModel
from ..league import League
from ..league_model import LeagueModel
from .combined_game_model import create_combined_game_model


class CombinedLeagueModel(LeagueModel):
    """The class implementing the combined league model."""

    def __init__(
        self,
        session: requests.Session,
        league: League,
        league_models: list[LeagueModel],
    ) -> None:
        super().__init__(league, session)
        self._league_models = league_models

    @classmethod
    def team_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different teams identities to a consistent identity."""
        raise NotImplementedError(
            "team_identity_map not implemented on CombinedLeagueModel parent class."
        )

    @classmethod
    def venue_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different venue identities to a consistent identity."""
        raise NotImplementedError(
            "venue_identity_map not implemented on CombinedLeagueModel parent class."
        )

    @property
    def games(self) -> Iterator[GameModel]:
        games: dict[str, list[GameModel]] = {}
        team_identity_map = self.team_identity_map()
        for league_model in self._league_models:
            for game_model in tqdm.tqdm(league_model.games, desc="Games from league"):
                game_components = [str(game_model.dt.date())]
                for team in game_model.teams:
                    if team.identifier not in team_identity_map:
                        logging.warning(
                            "%s for team %s not found in team identity map.",
                            team.identifier,
                            team.name,
                        )
                    team_identifier = team_identity_map.get(
                        team.identifier, team.identifier
                    )
                    game_components.append(team_identifier)
                game_components = sorted(game_components)
                key = "-".join(game_components)
                games[key] = games.get(key, []) + [game_model]
        for game_models in games.values():
            yield create_combined_game_model(  # type: ignore
                game_models,
                self.venue_identity_map(),
                team_identity_map,
            )
