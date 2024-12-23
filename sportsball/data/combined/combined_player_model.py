"""Combined player model."""

from typing import Optional

import requests

from ..player_model import PlayerModel


class CombinedPlayerModel(PlayerModel):
    """Combined implementation of the player model."""

    def __init__(
        self, session: requests.Session, player_models: list[PlayerModel]
    ) -> None:
        super().__init__(session)
        self._player_models = player_models

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._player_models[0].identifier

    @property
    def jersey(self) -> Optional[str]:
        """Return the jersey."""
        jersey = None
        for player_model in self._player_models:
            jersey = player_model.jersey
            if jersey is not None:
                break
        return jersey
