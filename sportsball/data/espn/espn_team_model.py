"""ESPN team model."""

# pylint: disable=too-many-arguments
import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import requests_cache

from ..odds_model import OddsModel
from ..player_model import PlayerModel
from ..team_model import TeamModel
from .espn_odds_model import ESPNOddsModel
from .espn_player_model import ESPNPlayerModel


class ESPNTeamModel(TeamModel):
    """ESPN implementation of the team model."""

    def __init__(
        self,
        session: requests_cache.CachedSession,
        team: Dict[str, Any],
        roster_dict: Dict[str, Any],
        odds: Sequence[OddsModel],
        score_dict: dict[str, Any],
    ) -> None:
        super().__init__(session)
        self._identifier = team["id"]

        name = team.get("name", team.get("fullName", team.get("displayName")))
        if name is None:
            raise ValueError("name is null")
        self._name = name

        self._location = team["location"]
        self._players = []
        for entity in roster_dict.get("entries", []):
            player = ESPNPlayerModel(session, entity)
            self._players.append(player)
        self._odds = odds
        self._points = score_dict["value"]

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @property
    def location(self) -> str | None:
        """Return the location."""
        return self._location

    @property
    def players(self) -> Sequence[PlayerModel]:
        """Return a list of players in the team."""
        return self._players

    @property
    def odds(self) -> Sequence[OddsModel]:
        """Return the odds."""
        return self._odds

    @property
    def points(self) -> float | None:
        """Return the points scored in the game."""
        return self._points

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **ESPNPlayerModel.urls_expire_after(),
            **ESPNOddsModel.urls_expire_after(),
        }
