"""The prototype class for a game."""

import datetime
from typing import Literal

import pytz
from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType
from .league import League
from .season_type import SeasonType
from .team_model import TeamModel
from .venue_model import VenueModel

GAME_DT_COLUMN = "dt"
SEASON_TYPE_COLUMN = "season_type"
SEASON_YEAR_COLUMN = "year"
VENUE_COLUMN_PREFIX: Literal["venue"] = "venue"
TEAM_COLUMN_PREFIX: Literal["teams"] = "teams"
GAME_ATTENDANCE_COLUMN: Literal["attendance"] = "attendance"
GAME_WEEK_COLUMN: Literal["week"] = "week"


def localize(venue: VenueModel | None, dt: datetime.datetime) -> datetime.datetime:
    """Localize the datetime against the timezone of the venue."""
    if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
        return dt
    tz = None
    venue_model = venue
    if venue_model is not None:
        address = venue_model.address
        if address is not None:
            timezone = address.timezone
            if timezone is not None:
                tz = pytz.timezone(timezone)
    if tz is None:
        tz = pytz.utc
    return tz.localize(dt)


class GameModel(BaseModel):
    """The serialisable representation of a game."""

    dt: datetime.datetime
    week: int | None = Field(..., alias=GAME_WEEK_COLUMN)
    game_number: int | None
    venue: VenueModel | None = Field(..., alias=VENUE_COLUMN_PREFIX)
    teams: list[TeamModel] = Field(..., alias=TEAM_COLUMN_PREFIX)
    end_dt: datetime.datetime | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD}
    )
    attendance: int | None = Field(..., alias=GAME_ATTENDANCE_COLUMN)
    league: League
    year: int | None
    season_type: SeasonType | None
