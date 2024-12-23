"""NFL SportsDB team model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import requests

from ...player_model import PlayerModel
from ...team_model import TeamModel


class NFLSportsDBTablesTeamModel(TeamModel):
    """NFL SportsDB implementation of the team model."""

    def __init__(
        self,
        session: requests.Session,
        team_id: str,
        name: str,
        points: float,
    ) -> None:
        super().__init__(session)
        self._identifier = team_id
        self._name = name
        self._points = points

    @property
    def players(self) -> Sequence[PlayerModel]:
        return []

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

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
        return {}
