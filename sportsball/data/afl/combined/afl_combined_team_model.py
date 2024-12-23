"""AFL combined team model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Sequence, Type, Union

from ...combined.combined_team_model import CombinedTeamModel
from ...odds_model import OddsModel
from ..afltables.afl_afltables_team_model import AFLAFLTablesTeamModel
from ..aussportsbetting.afl_aussportsbetting_odds_model import \
    AFLAusSportsBettingOddsModel
from .afl_combined_player_model import AFLCombinedPlayerModel


class AFLCombinedTeamModel(CombinedTeamModel):
    """AFL combined implementation of the team model."""

    @classmethod
    def _combined_player_model_class(cls) -> Type[AFLCombinedPlayerModel]:
        return AFLCombinedPlayerModel

    @classmethod
    def team_identity_map(cls) -> dict[str, str]:
        # pylint: disable=too-many-locals
        fitzroy = "fitzroy_idx"
        carlton = "carlton_idx"
        collingwood = "collingwood_idx"
        stkilda = "stkilda_idx"
        geelong = "geelong_idx"
        essendon = "essendon_idx"
        swans = "swans_idx"
        melbourne = "melbourne_idx"
        university = "university_idx"
        richmond = "richmond_idx"
        bulldogs = "bullldogs_idx"
        kangaroos = "kangaroos_idx"
        hawthorn = "hawthorn_idx"
        brisbane = "brisbaneb_idx"
        westcoast = "westcoast_idx"
        adelaide = "adelaide_idx"
        fremantle = "fremantle_idx"
        brisbane_lions = "brisbanel_idx"
        port_adelaide = "padelaide_idx"
        gws = "gws_idx"
        goldcoast = "goldcoast_idx"
        return {
            "fitzroy_idx": fitzroy,
            "carlton_idx": carlton,
            "collingwood_idx": collingwood,
            "stkilda_idx": stkilda,
            "geelong_idx": geelong,
            "essendon_idx": essendon,
            "swans_idx": swans,
            "melbourne_idx": melbourne,
            "university_idx": university,
            "richmond_idx": richmond,
            "bullldogs_idx": bulldogs,
            "kangaroos_idx": kangaroos,
            "hawthorn_idx": hawthorn,
            "brisbaneb_idx": brisbane,
            "westcoast_idx": westcoast,
            "adelaide_idx": adelaide,
            "fremantle_idx": fremantle,
            "brisbanel_idx": brisbane_lions,
            "padelaide_idx": port_adelaide,
            "gws_idx": gws,
            "goldcoast_idx": goldcoast,
        }

    @property
    def odds(self) -> Sequence[OddsModel]:
        """Return the odds."""
        odds: list[OddsModel] = []
        try:
            odds.append(
                AFLAusSportsBettingOddsModel(self.session, self._date, self.name)
            )
        except ValueError as e:
            if self._date.year >= 2010:
                raise e
        for team_model in self._team_models:
            odds.extend(team_model.odds)
        return odds

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **AFLAFLTablesTeamModel.urls_expire_after(),
            **AFLCombinedPlayerModel.urls_expire_after(),
            **AFLAusSportsBettingOddsModel.urls_expire_after(),
        }
