"""NFL season model."""

# pylint: disable=line-too-long
import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests_cache

from ..game_model import GameModel
from ..season_model import SeasonModel
from ..season_type import SeasonType
from .nfl_game_model import NFLGameModel


def _season_type_from_name(name: str) -> SeasonType:
    if name == "Regular Season":
        return SeasonType.REGULAR
    if name == "Preseason":
        return SeasonType.PRESEASON
    if name == "Postseason":
        return SeasonType.POSTSEASON
    if name == "Off Season":
        return SeasonType.OFFSEASON
    raise ValueError(f"Unrecognised season name: {name}")


class NFLSeasonModel(SeasonModel):
    """The class implementing the NFL season model."""

    def __init__(
        self, session: requests_cache.CachedSession, season: Dict[str, Any]
    ) -> None:
        super().__init__(
            season["year"], session, _season_type_from_name(season["name"])
        )
        self._season = season

    @property
    def games(self) -> Iterator[GameModel]:
        page = 1
        week_count = 0
        while True:
            weeks_response = self.session.get(
                self._season["weeks"]["$ref"] + f"&page={page}"
            )
            weeks_response.raise_for_status()
            weeks = weeks_response.json()
            for item in weeks["items"]:
                week_response = self.session.get(item["$ref"])
                week_response.raise_for_status()
                week = week_response.json()
                events_page = 1
                events_count = 0
                while True:
                    events_response = self.session.get(
                        week["events"]["$ref"] + f"&page={events_page}"
                    )
                    events = events_response.json()
                    for event_item in events["items"]:
                        event_response = self.session.get(event_item["$ref"])
                        event_response.raise_for_status()
                        event = event_response.json()
                        yield NFLGameModel(
                            event, week_count, events_count, self.session
                        )
                        events_count += 1
                    if events_page >= events["pageCount"]:
                        break
                    events_page += 1
                week_count += 1
            if page >= weeks["pageCount"]:
                break
            page += 1

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL caching rules."""
        current_year = datetime.datetime.now().year
        return {
            **{
                f"http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{current_year}/.*": datetime.timedelta(
                    hours=1
                ),
            },
            **NFLGameModel.urls_expire_after(),
        }
