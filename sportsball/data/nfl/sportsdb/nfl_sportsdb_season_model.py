"""NFL Sports DB season model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests

from ...game_model import GameModel
from ...season_model import SeasonModel
from ...season_type import SeasonType
from .nfl_sportsdb_game_model import NFLSportsDBGameModel


class NFLSportsDBSeasonModel(SeasonModel):
    """The class implementing the NFL SportsDB season model."""

    # pylint: disable=protected-access

    def __init__(
        self,
        session: requests.Session,
        season_year: str,
        season_type: SeasonType,
        league_id: str,
    ) -> None:
        super().__init__(session)
        self._season_year = season_year
        self._season_type = season_type
        self._league_id = league_id

    @property
    def year(self) -> int | None:
        """Return the year."""
        return int(self._season_year)

    @property
    def season_type(self) -> SeasonType | None:
        """Return the season type."""
        return self._season_type

    @property
    def games(self) -> Iterator[GameModel]:
        def produce_games(round_str: str, week: int) -> Iterator[GameModel]:
            # pylint: disable=line-too-long
            response = self.session.get(
                f"https://www.thesportsdb.com/api/v1/json/3/eventsround.php?id={self._league_id}&r={round_str}&s={self._season_year}"
            )
            response.raise_for_status()
            games = response.json()
            events = games["events"]
            if events is None:
                raise ValueError("events is null.")
            for count, game in enumerate(events):
                yield NFLSportsDBGameModel(self.session, game, week, count)

        match self._season_type:
            case SeasonType.OFFSEASON:
                return
            case SeasonType.PRESEASON:
                try:
                    yield from produce_games(str(500), 0)
                except ValueError:
                    pass
            case SeasonType.REGULAR:
                try:
                    for count, round_str in enumerate(range(1, 125)):
                        yield from produce_games(str(round_str), count)
                except ValueError:
                    pass
            case SeasonType.POSTSEASON:
                for count, round_str in enumerate([125, 150, 160, 170, 180, 200]):
                    try:
                        yield from produce_games(str(round_str), 21 + count)
                    except ValueError:
                        pass

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL caching rules."""
        return {
            **NFLSportsDBGameModel.urls_expire_after(),
        }
