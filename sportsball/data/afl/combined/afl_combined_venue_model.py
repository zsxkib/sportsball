"""AFL combined venue model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...combined.combined_venue_model import CombinedVenueModel
from ...google.google_address_model import GoogleAddressModel


class AFLCombinedVenueModel(CombinedVenueModel):
    """AFL combined implementation of the venue model."""

    @classmethod
    def venue_identity_map(cls) -> dict[str, str]:
        # pylint: disable=too-many-statements,too-many-locals
        brunswick_st = "brunswick_st"
        victoria_park = "victoria_park"
        corio_oval = "corio_oval"
        lake_oval = "lake_oval"
        east_melbourne = "east_melbourne"
        junction_oval = "junction_oval"
        mcg = "mcg"
        princes_park = "princes_park"
        scg = "scg"
        punt_rd = "punt_rd"
        windy_hill = "windy_hill"
        glenferrie_oval = "glenferrie_oval"
        arden_st = "arden_st"
        western_oval = "western_oval"
        olympic_park = "olympic_park"
        kardinia_park = "kardinia_park"
        yarraville_oval = "yarraville_oval"
        toorak_park = "toorak_park"
        euroa = "euroa"
        north_hobart = "north_hobart"
        yallourn = "yallourn"
        albury = "albury"
        brisbane_exhibition = "brisbane_exhibition"
        moorabbin_oval = "moorabbin_oval"
        coburg_oval = "coburg_oval"
        waverley_park = "waverley_park"
        subiaco = "subiaco"
        gabba = "gabba"
        carrara = "carrara"
        waca = "waca"
        football_park = "football_park"
        manuka_oval = "manuka_oval"
        docklands = "docklands"
        stadium_australia = "stadium_australia"
        york_park = "york_park"
        showground = "showground"
        marrara_oval = "marrara_oval"
        cazalys_stadium = "cazalys_stadium"
        adelaide_oval = "adelaide_oval"
        wellington = "wrs"
        bellerive_oval = "bellerive_oval"
        traeger = "traeger"
        jiangwan = "jiangwan"
        eureka = "eureka"
        perth = "perth"
        bruce_stadium = "bruce_stadium"
        blacktown = "blacktown"
        riverway = "riverway"
        norwood = "norwood"
        summit = "summit"
        return {
            "brunswick_st": brunswick_st,
            "victoria_park": victoria_park,
            "corio_oval": corio_oval,
            "lake_oval": lake_oval,
            "east_melbourne": east_melbourne,
            "junction_oval": junction_oval,
            "mcg": mcg,
            "princes_park": princes_park,
            "scg": scg,
            "punt_rd": punt_rd,
            "windy_hill": windy_hill,
            "glenferrie_oval": glenferrie_oval,
            "arden_st": arden_st,
            "western_oval": western_oval,
            "olympic_park": olympic_park,
            "kardinia_park": kardinia_park,
            "yarraville_oval": yarraville_oval,
            "toorak_park": toorak_park,
            "euroa": euroa,
            "north_hobart": north_hobart,
            "yallourn": yallourn,
            "albury": albury,
            "brisbane_exhibition": brisbane_exhibition,
            "moorabbin_oval": moorabbin_oval,
            "coburg_oval": coburg_oval,
            "waverley_park": waverley_park,
            "subiaco": subiaco,
            "gabba": gabba,
            "carrara": carrara,
            "waca": waca,
            "football_park": football_park,
            "manuka_oval": manuka_oval,
            "docklands": docklands,
            "stadium_australia": stadium_australia,
            "york_park": york_park,
            "showground": showground,
            "marrara_oval": marrara_oval,
            "cazalys_stadium": cazalys_stadium,
            "adelaide_oval": adelaide_oval,
            "wrs": wellington,
            "bellerive_oval": bellerive_oval,
            "traeger": traeger,
            "jiangwan": jiangwan,
            "eureka": eureka,
            "perth": perth,
            "bruce_stadium": bruce_stadium,
            "blacktown": blacktown,
            "riverway": riverway,
            "norwood": norwood,
            "summit": summit,
        }

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return GoogleAddressModel.urls_expire_after()
