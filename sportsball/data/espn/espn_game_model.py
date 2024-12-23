"""ESPN game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Union

import pytz
import requests
from dateutil.parser import parse

from ..game_model import GameModel
from ..odds_model import OddsModel
from ..team_model import TeamModel
from ..venue_model import VenueModel
from .espn_bookie_model import ESPNBookieModel
from .espn_odds_model import MONEYLINE_KEY, ESPNOddsModel
from .espn_team_model import ESPNTeamModel
from .espn_venue_model import ESPNVenueModel


def _create_espn_team(
    competitor: Dict[str, Any],
    odds_dict: Dict[str, Any],
    session: requests.Session,
) -> ESPNTeamModel:
    team_response = session.get(competitor["team"]["$ref"])
    team_response.raise_for_status()
    team_dict = team_response.json()

    odds_key = competitor["homeAway"] + "TeamOdds"
    odds: Sequence[OddsModel] = []
    if odds_dict:
        odds = [
            ESPNOddsModel(
                session,
                x[odds_key],
                ESPNBookieModel(session, x["provider"]),
            )
            for x in odds_dict["items"]
            if odds_key in x and MONEYLINE_KEY in x[odds_key]
        ]

    roster_dict = {}
    if "roster" in competitor:
        roster_response = session.get(competitor["roster"]["$ref"])
        roster_response.raise_for_status()
        roster_dict = roster_response.json()

    score_response = session.get(competitor["score"]["$ref"])
    score_response.raise_for_status()
    score_dict = score_response.json()

    return ESPNTeamModel(session, team_dict, roster_dict, odds, score_dict)


class ESPNGameModel(GameModel):
    """ESPN implementation of the game model."""

    def __init__(
        self,
        event: Dict[str, Any],
        week: int,
        game_number: int,
        session: requests.Session,
    ) -> None:
        super().__init__(session)
        self._dt = parse(event["date"])
        self._week = week
        self._game_number = game_number
        venue = None
        if "venue" in event:
            venue = ESPNVenueModel(session, event["venue"], self._dt)
        if venue is None and "venues" in event:
            venues = event["venues"]
            if venues:
                venue_url = event["venues"][0]["$ref"]
                venue_response = session.get(venue_url)
                venue_response.raise_for_status()
                venue = ESPNVenueModel(session, venue_response.json(), self._dt)
        self._venue = venue

        self._teams = []
        self._attendance = None
        for competition in event["competitions"]:
            odds_dict = {}
            if "odds" in competition:
                odds_response = session.get(competition["odds"]["$ref"])
                odds_response.raise_for_status()
                odds_dict = odds_response.json()

            for competitor in competition["competitors"]:
                self._teams.append(_create_espn_team(competitor, odds_dict, session))
            self._attendance = competition["attendance"]

    @property
    def dt(self) -> datetime.datetime:
        """Return the game time."""
        dt = self._dt
        if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
            return dt
        tz = None
        venue_model = self.venue
        if venue_model is not None:
            address = venue_model.address
            if address is not None:
                timezone = address.timezone
                if timezone is not None:
                    tz = pytz.timezone(timezone)
        if tz is None:
            tz = pytz.utc
        return tz.localize(dt)

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

    @property
    def attendance(self) -> int | None:
        """Return the attendance at the game."""
        return self._attendance

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **ESPNVenueModel.urls_expire_after(),
            **ESPNTeamModel.urls_expire_after(),
        }
