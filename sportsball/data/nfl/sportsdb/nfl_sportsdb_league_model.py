"""NFL Sports DB league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests

from ...league import League
from ...league_model import LeagueModel
from ...season_model import SeasonModel
from ...season_type import SeasonType
from .nfl_sportsdb_season_model import NFLSportsDBSeasonModel


class NFLSportsDBLeagueModel(LeagueModel):
    """NFL SportsDB implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.NFL, session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        """Find the seasons represented by the league."""
        league_id = "4391"
        response = self.session.get(
            f"https://www.thesportsdb.com/api/v1/json/3/search_all_seasons.php?id={league_id}"
        )
        response.raise_for_status()
        seasons = response.json()
        for season in seasons["seasons"]:
            season_year = season["strSeason"]
            for season_type in SeasonType:
                yield NFLSportsDBSeasonModel(
                    self.session, season_year, season_type, league_id
                )

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
        }
