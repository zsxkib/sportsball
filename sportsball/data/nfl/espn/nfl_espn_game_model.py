"""NFL game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import requests_cache
from dateutil.parser import parse

from ...game_model import GameModel
from ...odds_model import OddsModel
from ...team_model import TeamModel
from ...venue_model import VenueModel
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
    odds: Sequence[OddsModel] = []
    if odds_dict:
        odds = [
            NFLESPNOddsModel(
                session,
                x[odds_key],
                NFLESPNBookieModel(session, x["provider"]),
            )
            for x in odds_dict["items"]
            if odds_key in x and MONEYLINE_KEY in x[odds_key]
        ]

    roster_dict = {}
    if "roster" in competitor:
        roster_response = session.get(competitor["roster"]["$ref"])
        roster_response.raise_for_status()
        roster_dict = roster_response.json()

    return NFLESPNTeamModel(session, team_dict, roster_dict, odds)


class NFLESPNGameModel(GameModel):
    """NFL implementation of the game model."""

    def __init__(
        self,
        event: Dict[str, Any],
        week: int,
        game_number: int,
        session: requests_cache.CachedSession,
    ) -> None:
        super().__init__(session)
        self._dt = parse(event["date"])
        self._week = week
        self._game_number = game_number
        venue = None
        if "venue" in event:
            venue = NFLESPNVenueModel(session, event["venue"])
        self._venue = venue

        self._teams = []
        for competition in event["competitions"]:
            odds_dict = {}
            if "odds" in competition:
                odds_response = session.get(competition["odds"]["$ref"])
                odds_response.raise_for_status()
                odds_dict = odds_response.json()

            for competitor in competition["competitors"]:
                self._teams.append(_create_nfl_team(competitor, odds_dict, session))

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        return self._dt

    @property
    def week(self) -> int:
        """Return the game week."""
        return self._week

    @property
    def game_number(self) -> int:
        """Return the game number."""
        return self._game_number

    @property
    def venue(self) -> Optional[VenueModel]:
        """Return the venue the game was played at."""
        return self._venue

    @property
    def teams(self) -> Sequence[TeamModel]:
        """Return the teams within the game."""
        return self._teams

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
