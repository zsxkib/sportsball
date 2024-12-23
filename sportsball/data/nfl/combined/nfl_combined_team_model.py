"""NFL combined team model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Type, Union

from ...combined.combined_team_model import CombinedTeamModel
from ..espn.nfl_espn_team_model import NFLESPNTeamModel
from ..sportsdb.nfl_sportsdb_team_model import NFLSportsDBTablesTeamModel
from .nfl_combined_player_model import NFLCombinedPlayerModel


class NFLCombinedTeamModel(CombinedTeamModel):
    """NFL combined implementation of the team model."""

    @classmethod
    def _combined_player_model_class(cls) -> Type[NFLCombinedPlayerModel]:
        return NFLCombinedPlayerModel

    @classmethod
    def team_identity_map(cls) -> dict[str, str]:
        # pylint: disable=too-many-locals
        los_angeles_rams = "135907"
        chicago_bears = "134938"
        houstan_texans = "134926"
        new_york_giants = "134935"
        detroit_lions = "134939"
        new_england_patriots = "134920"
        carolina_panthers = "134943"
        pittsburgh_stealers = "134925"
        miami_dolphins = "134919"
        atlanta_falcons = "134942"
        baltimore_ravens = "134922"
        philadelphia_eagles = "134936"
        new_york_jets = "134921"
        washington_commanders = "134937"
        buffalo_bills = "134918"
        minnesota_vikings = "134941"
        las_vegas_raiders = "134932"
        cleveland_browns = "134924"
        green_bay_packers = "134940"
        jacksonville_jaguars = "134928"
        kansas_city_chiefs = "134931"
        tennessee_titans = "134929"
        san_francisco_49ers = "134948"
        cincinatti_bengals = "134923"
        tampa_bay_buccaneers = "134945"
        los_angeles_chargers = "135908"
        seattle_seahawks = "134949"
        arizona_cardinals = "134946"
        new_orleans_saints = "134944"
        indianapolis_colts = "134927"
        denver_broncos = "134930"
        dallas_cowboys = "134934"
        american_football_conference = "31"
        national_football_conference = "32"
        return {
            "135907": los_angeles_rams,
            "134938": chicago_bears,
            "134926": houstan_texans,
            "134935": new_york_giants,
            "134939": detroit_lions,
            "134920": new_england_patriots,
            "134943": carolina_panthers,
            "134925": pittsburgh_stealers,
            "134919": miami_dolphins,
            "134942": atlanta_falcons,
            "134922": baltimore_ravens,
            "134936": philadelphia_eagles,
            "134921": new_york_jets,
            "134937": washington_commanders,
            "134918": buffalo_bills,
            "134941": minnesota_vikings,
            "134932": las_vegas_raiders,
            "134924": cleveland_browns,
            "134940": green_bay_packers,
            "134928": jacksonville_jaguars,
            "134931": kansas_city_chiefs,
            "134929": tennessee_titans,
            "134948": san_francisco_49ers,
            "134923": cincinatti_bengals,
            "134945": tampa_bay_buccaneers,
            "135908": los_angeles_chargers,
            "134949": seattle_seahawks,
            "134946": arizona_cardinals,
            "134944": new_orleans_saints,
            "134927": indianapolis_colts,
            "134930": denver_broncos,
            "134934": dallas_cowboys,
            "5": cleveland_browns,
            "20": new_york_jets,
            "17": new_england_patriots,
            "34": houstan_texans,
            "26": seattle_seahawks,
            "16": minnesota_vikings,
            "4": cincinatti_bengals,
            "9": green_bay_packers,
            "8": detroit_lions,
            "19": new_york_giants,
            "15": miami_dolphins,
            "1": atlanta_falcons,
            "27": tampa_bay_buccaneers,
            "23": pittsburgh_stealers,
            "28": washington_commanders,
            "22": arizona_cardinals,
            "7": denver_broncos,
            "2": buffalo_bills,
            "11": indianapolis_colts,
            "3": chicago_bears,
            "10": tennessee_titans,
            "29": carolina_panthers,
            "6": dallas_cowboys,
            "30": jacksonville_jaguars,
            "33": baltimore_ravens,
            "21": philadelphia_eagles,
            "14": los_angeles_rams,
            "24": los_angeles_chargers,
            "18": new_orleans_saints,
            "12": kansas_city_chiefs,
            "13": las_vegas_raiders,
            "25": san_francisco_49ers,
            "31": american_football_conference,
            "32": national_football_conference,
            "134933": los_angeles_chargers,
            "134947": los_angeles_rams,
            "135834": los_angeles_rams,
        }

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **NFLSportsDBTablesTeamModel.urls_expire_after(),
            **NFLESPNTeamModel.urls_expire_after(),
            **NFLCombinedPlayerModel.urls_expire_after(),
        }
