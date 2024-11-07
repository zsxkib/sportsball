"""NFL odds model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...bookie_model import BookieModel
from ...team_model import OddsModel
from .nfl_espn_bookie_model import NFLESPNBookieModel

MONEYLINE_KEY = "moneyLine"


class NFLESPNOddsModel(OddsModel):
    """NFL implementation of the odds model."""

    def __init__(self, odds: Dict[str, Any], bookie: BookieModel) -> None:
        odds_val = 0.0
        moneyline = odds[MONEYLINE_KEY]
        if moneyline > 0:
            odds_val = (float(moneyline) / 100.0) + 1.0
        elif moneyline < 0:
            odds_val = (100.0 / float(abs(moneyline))) + 1.0
        super().__init__(odds_val, bookie)

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return NFLESPNBookieModel.urls_expire_after()
