"""NBA NBA league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests

from ...league import League
from ...league_model import LeagueModel
from ...season_model import SeasonModel


class NBANBALeagueModel(LeagueModel):
    """NBA NBA implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.NBA, session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        """Find the seasons represented by the league."""
        raise NotImplementedError("season not implemented by LeagueModel parent class.")

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            # **NBAESPNSeasonModel.urls_expire_after(),
        }
