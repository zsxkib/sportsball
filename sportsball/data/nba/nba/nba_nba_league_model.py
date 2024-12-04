"""NBA NBA league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import pandas as pd
import requests
from nba_api.stats.endpoints import leaguegamefinder  # type: ignore

from ...league import League
from ...league_model import LeagueModel
from ...season_model import SeasonModel
from .nba_nba_season_model import NBANBASeasonModel


def _combine_team_games(df: pd.DataFrame, keep_method="home") -> pd.DataFrame:
    """Combine a TEAM_ID-GAME_ID unique table into rows by game. Slow.

    Parameters
    ----------
    df : Input DataFrame.
    keep_method : {'home', 'away', 'winner', 'loser', ``None``}, default 'home'
        - 'home' : Keep rows where TEAM_A is the home team.
        - 'away' : Keep rows where TEAM_A is the away team.
        - 'winner' : Keep rows where TEAM_A is the losing team.
        - 'loser' : Keep rows where TEAM_A is the winning team.
        - ``None`` : Keep all rows. Will result in an output DataFrame the same
            length as the input DataFrame.

    Returns
    -------
    result : DataFrame
    """
    # Join every row to all others with the same game ID.
    joined = pd.merge(
        df, df, suffixes=["_A", "_B"], on=["SEASON_ID", "GAME_ID", "GAME_DATE"]
    )
    # Filter out any row that is joined to itself.
    result = joined[joined.TEAM_ID_A != joined.TEAM_ID_B]
    # Take action based on the keep_method flag.
    if keep_method is None:
        # Return all the rows.
        pass
    elif keep_method.lower() == "home":
        # Keep rows where TEAM_A is the home team.
        result = result[result.MATCHUP_A.str.contains(" vs. ")]
    elif keep_method.lower() == "away":
        # Keep rows where TEAM_A is the away team.
        result = result[result.MATCHUP_A.str.contains(" @ ")]
    elif keep_method.lower() == "winner":
        result = result[result.WL_A == "W"]
    elif keep_method.lower() == "loser":
        result = result[result.WL_A == "L"]
    else:
        raise ValueError(f"Invalid keep_method: {keep_method}")
    return result


class NBANBALeagueModel(LeagueModel):
    """NBA NBA implementation of the league model."""

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.NBA, session)

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        """Find the seasons represented by the league."""
        df = None
        while df is None or df.empty:
            date_to = ""
            if df is not None:
                date_to = df["GAME_DATE"].min().strftime("%m/%d/%Y")
            gamefinder = leaguegamefinder.LeagueGameFinder(date_to_nullable=date_to)
            dfs = gamefinder.get_data_frames()
            df = dfs[0]
            for _, group_df in df.groupby(by="SEASON_ID"):
                yield NBANBASeasonModel(self.session, _combine_team_games(group_df))

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **NBANBASeasonModel.urls_expire_after(),
        }
