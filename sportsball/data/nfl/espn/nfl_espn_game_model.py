"""NFL game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests_cache
from dateutil.parser import parse

from ...game_model import GameModel
from ...odds_model import OddsModel
from ...team_model import TeamModel
from .nfl_espn_bookie_model import NFLESPNBookieModel
from .nfl_espn_odds_model import MONEYLINE_KEY, NFLESPNOddsModel
from .nfl_espn_team_model import NFLESPNTeamModel
from .nfl_espn_venue_model import NFLESPNVenueModel


def _create_nfl_team(
    competitor: Dict[str, Any],
    odds_dict: Dict[str, Any],
    session: requests_cache.CachedSession,
) -> NFLESPNTeamModel:
    team_response = session.get(competitor["team"]["$ref"])
    team_response.raise_for_status()
    team_dict = team_response.json()

    odds_key = competitor["homeAway"] + "TeamOdds"
    odds: Dict[str, OddsModel] = {}
    if odds_dict:
        odds = {
            x["provider"]["id"]: NFLESPNOddsModel(
                x[odds_key],
                NFLESPNBookieModel(x["provider"]),
            )
            for x in odds_dict["items"]
            if odds_key in x and MONEYLINE_KEY in x[odds_key]
        }

    roster_dict = {}
    if "roster" in competitor:
        roster_response = session.get(competitor["roster"]["$ref"])
        roster_response.raise_for_status()
        roster_dict = roster_response.json()

    return NFLESPNTeamModel(team_dict, roster_dict, odds)


class NFLESPNGameModel(GameModel):
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
            venue = NFLESPNVenueModel(event["venue"])

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
            **NFLESPNVenueModel.urls_expire_after(),
            **NFLESPNTeamModel.urls_expire_after(),
        }
