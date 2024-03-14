"""NFL league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests_cache

from ..league import League
from ..league_model import LeagueModel
from ..season_model import SeasonModel
from .nfl_season_model import NFLSeasonModel

_SEASON_URL = (
    "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons?limit=100"
)


class NFLLeagueModel(LeagueModel):
    """NFL implementation of the league model."""

    def __init__(self, session: requests_cache.CachedSession) -> None:
        super().__init__(League.NFL, session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        page = 1
        while True:
            response = self.session.get(_SEASON_URL + f"&page={page}")
            seasons = response.json()
            for item in seasons["items"]:
                season_response = self.session.get(item["$ref"])
                season_response.raise_for_status()
                season_json = season_response.json()

                for season_item in season_json["types"]["items"]:
                    season_type_response = self.session.get(season_item["$ref"])
                    season_type_response.raise_for_status()
                    season_type_json = season_type_response.json()
                    yield NFLSeasonModel(self.session, season_type_json)

            if page >= seasons["pageCount"]:
                break
            page += 1

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **NFLSeasonModel.urls_expire_after(),
            **{
                _SEASON_URL + ".*": datetime.timedelta(hours=1),
            },
        }
