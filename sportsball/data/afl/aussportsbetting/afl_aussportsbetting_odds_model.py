"""AFL aussportsbetting odds model."""

import datetime
from io import BytesIO
from typing import Any, Dict, Optional, Pattern, Union

import requests_cache
from dateutil.parser import parse
from openpyxl import Workbook, load_workbook

from ...bookie_model import BookieModel
from ...team_model import OddsModel
from .afl_aussportsbetting_bookie_model import AFLAusSportsBettingBookieModel

_ODDS_XLSX_URL = "https://www.aussportsbetting.com/historical_data/afl.xlsx"
_WORKBOOK: Workbook | None = None
_TEAM_NAME_TRANSLATIONS = {
    "Greater Western Sydney": "GWS Giants",
    "Brisbane Lions": "Brisbane",
}


class AFLAusSportsBettingOddsModel(OddsModel):
    """AFL aus sports betting implementation of the odds model."""

    def __init__(
        self, session: requests_cache.CachedSession, date: datetime.date, team_name: str
    ) -> None:
        # pylint: disable=global-statement
        global _WORKBOOK
        team_name = _TEAM_NAME_TRANSLATIONS.get(team_name, team_name)
        super().__init__(session)
        if _WORKBOOK is None:
            response = session.get(_ODDS_XLSX_URL)
            _WORKBOOK = load_workbook(filename=BytesIO(response.content))
        ws = _WORKBOOK.active
        if ws is None:
            raise ValueError("ws is null.")
        odds = None
        for row in ws.iter_rows():
            date_cell = str(row[0].value)
            if date_cell in {"Date", "None"}:
                continue
            potential_date = parse(date_cell).date()
            if date != potential_date:
                continue
            home_team = str(row[2].value).strip()
            if home_team == team_name:
                odds = float(str(row[12].value))
                break
            away_team = str(row[3].value).strip()
            if away_team == team_name:
                odds = float(str(row[13].value))
                break
        if odds is None:
            raise ValueError(f"odds is null with date {date} team_name {team_name}.")
        self._odds_val = odds

    @property
    def odds(self) -> float:
        """Return the odds."""
        return self._odds_val

    @property
    def bookie(self) -> BookieModel:
        """Return the bookie."""
        return AFLAusSportsBettingBookieModel(self.session)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **{
                _ODDS_XLSX_URL: datetime.timedelta(hours=1),
            },
            **AFLAusSportsBettingBookieModel.urls_expire_after(),
        }
