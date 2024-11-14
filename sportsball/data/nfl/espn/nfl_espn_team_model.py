"""NFL team model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import requests_cache

from ...odds_model import OddsModel
from ...player_model import PlayerModel
from ...team_model import TeamModel
from .nfl_espn_odds_model import NFLESPNOddsModel
from .nfl_espn_player_model import NFLESPNPlayerModel


class NFLESPNTeamModel(TeamModel):
    """NFL implementation of the team model."""

    def __init__(
        self,
        session: requests_cache.CachedSession,
        team: Dict[str, Any],
        roster_dict: Dict[str, Any],
        odds: Sequence[OddsModel],
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
            player = NFLESPNPlayerModel(session, entity)
            self._players.append(player)
        self._odds = odds

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

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **NFLESPNPlayerModel.urls_expire_after(),
            **NFLESPNOddsModel.urls_expire_after(),
        }
