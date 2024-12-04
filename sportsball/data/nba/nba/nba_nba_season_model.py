"""NBA NBA season model."""

# pylint: disable=line-too-long
import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import pandas as pd
import requests

from ...game_model import GameModel
from ...season_model import SeasonModel
from ...season_type import SeasonType
from .nba_nba_game_model import NBANBAGameModel


class NBANBASeasonModel(SeasonModel):
    """The class implementing the NBA NBA season model."""

    def __init__(self, session: requests.Session, df: pd.DataFrame) -> None:
        super().__init__(session)
        self._df = df

    @property
    def year(self) -> int | None:
        """Return the year."""
        season = self._df["SEASON_ID"].iloc[0]
        return int(season[1:])

    @property
    def season_type(self) -> SeasonType | None:
        """Return the season type."""
        return SeasonType.REGULAR

    @property
    def games(self) -> Iterator[GameModel]:
        return  # type: ignore

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL caching rules."""
        return {
            **NBANBAGameModel.urls_expire_after(),
        }
