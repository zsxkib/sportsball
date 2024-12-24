"""NBA NBA league model."""

from typing import Iterator

import pandas as pd
import requests

from ...game_model import GameModel
from ...league import League
from ...league_model import LeagueModel


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
    def games(self) -> Iterator[GameModel]:
        return  # type: ignore
