"""NFL game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests_cache
from dateutil.parser import parse

from ..game_model import GameModel
from ..odds_model import OddsModel
from ..team_model import TeamModel
from .nfl_bookie_model import NFLBookieModel
from .nfl_odds_model import MONEYLINE_KEY, NFLOddsModel
from .nfl_team_model import NFLTeamModel
from .nfl_venue_model import NFLVenueModel


def _create_nfl_team(
    competitor: Dict[str, Any],
    odds_dict: Dict[str, Any],
    session: requests_cache.CachedSession,
) -> NFLTeamModel:
    team_response = session.get(competitor["team"]["$ref"])
    team_response.raise_for_status()
    team_dict = team_response.json()

    odds_key = competitor["homeAway"] + "TeamOdds"
    odds: Dict[str, OddsModel] = {}
    if odds_dict:
        odds = {
            x["provider"]["id"]: NFLOddsModel(
                x[odds_key],
                NFLBookieModel(x["provider"]),
            )
            for x in odds_dict["items"]
            if odds_key in x and MONEYLINE_KEY in x[odds_key]
        }

    roster_dict = {}
    if "roster" in competitor:
        roster_response = session.get(competitor["roster"]["$ref"])
        roster_response.raise_for_status()
        roster_dict = roster_response.json()

    return NFLTeamModel(team_dict, roster_dict, odds)


class NFLGameModel(GameModel):
    """NFL implementation of the game model."""

    def __init__(
        self,
        event: Dict[str, Any],
        week: int,
        game_number: int,
        session: requests_cache.CachedSession,
    ) -> None:
        dt = parse(event["date"])
        venue = None
        if "venue" in event:
            venue = NFLVenueModel(event["venue"])

        teams = []
        for competition in event["competitions"]:
            odds_dict = {}
            if "odds" in competition:
                odds_response = session.get(competition["odds"]["$ref"])
                odds_response.raise_for_status()
                odds_dict = odds_response.json()

            for competitor in competition["competitors"]:
                teams.append(_create_nfl_team(competitor, odds_dict, session))

        super().__init__(dt, week, game_number, venue, teams, session)

    @property
    def home_team(self) -> TeamModel:
        return self._teams[0]

    @property
    def away_team(self) -> TeamModel:
        return self._teams[1]

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **NFLVenueModel.urls_expire_after(),
            **NFLTeamModel.urls_expire_after(),
        }
