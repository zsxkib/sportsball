"""NFL combined venue model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...combined.combined_venue_model import CombinedVenueModel
from ...google.google_address_model import GoogleAddressModel


class NFLCombinedVenueModel(CombinedVenueModel):
    """NFL combined implementation of the venue model."""

    @classmethod
    def venue_identity_map(cls) -> dict[str, str]:
        # pylint: disable=too-many-statements,too-many-locals
        empower_field = "18784"
        tom_bensom_hall_of_fame_stadium = "28739"
        metlife_stadium = "15812"
        gilette_stadium = "15816"
        acrisure_stadium = "29572"
        hard_rock_stadium = "20373"
        mtt_bank_stadium = "21598"
        highmark_stadium = "30812"
        us_bank_stadium = "15803"
        cleveland_browns_stadium = "29570"
        everbank_stadium = "29576"
        nissan_stadium = "30912"
        paycor_stadium = "29569"
        sofi_stadium = "23720"
        state_farm_stadium = "16027"
        lucas_oil_stadium = "15807"
        nrg_stadium = "15873"
        soldier_field = "16092"
        arrowhead_stadium = "29575"
        bank_of_america_stadium = "18776"
        allegiant_stadium = "21293"
        levis_stadium = "16090"
        mercedez_benz_stadium = "16029"
        raymond_james_stadium = "15874"
        lambeau_field = "17146"
        lincoln_financial_field = "16094"
        ford_field = "15808"
        att_stadium = "15802"
        lumen_field = "19833"
        caesars_superdome = "29571"
        neo_quimica_arena = "16461"
        fedex_field = "29574"
        tottenham_hotspur_stadium = "16118"
        wembley_stadium = "16163"
        allianz_arena = "15537"
        deutsche_bank_park = "17590"
        camping_world_stadium = "4013"
        estadio_azteca = "1850"
        dignity_health_sports_park = "538"
        oakland_coliseum = "3867"
        los_angeles_memorial_coliseum = "477"
        twickenham_stadium = "5128"
        georgia_dome = "3495"
        sdccu_stadium = "3932"
        trans_world_dome = "3494"
        candlestick_park = "3669"
        rogers_centre = "1822"
        aloha_stadium = "3610"
        texas_stadium = "3954"
        mountain_america_stadium = "3947"
        silverdome = "3929"
        liberty_bowl_memorial_stadium = "21515"
        rfk_stadium = "18381"
        vanderbilt_stadium = "21572"
        rose_bowl = "16093"
        miami_orange_bowl = "20447"
        stanford_stadium = "18382"
        milwaukee_county_stadium = "30850"
        shea_stadium = "21813"
        yale_bowl = "21608"
        tiger_stadium = "21532"
        war_memorial_stadium = "21581"
        yankee_stadium = "19474"
        municipal_stadium = "21642"
        cotton_bowl = "18378"
        kezar_stadium = "25773"
        franklin_field = "21659"
        wrigley_field = "30763"
        city_stadium = "19533"
        ig_field = "4461"
        rice_stadium = "21557"
        independence_stadium = "3766"
        memorial_stadium = "16280"
        return {
            "18784": empower_field,
            "28739": tom_bensom_hall_of_fame_stadium,
            "15812": metlife_stadium,
            "15816": gilette_stadium,
            "29572": acrisure_stadium,
            "20373": hard_rock_stadium,
            "21598": mtt_bank_stadium,
            "30812": highmark_stadium,
            "15803": us_bank_stadium,
            "29570": cleveland_browns_stadium,
            "29576": everbank_stadium,
            "30912": nissan_stadium,
            "29569": paycor_stadium,
            "23720": sofi_stadium,
            "16027": state_farm_stadium,
            "15807": lucas_oil_stadium,
            "15873": nrg_stadium,
            "16092": soldier_field,
            "29575": arrowhead_stadium,
            "18776": bank_of_america_stadium,
            "21293": allegiant_stadium,
            "16090": levis_stadium,
            "16029": mercedez_benz_stadium,
            "15874": raymond_james_stadium,
            "17146": lambeau_field,
            "16094": lincoln_financial_field,
            "15808": ford_field,
            "15802": att_stadium,
            "19833": lumen_field,
            "29571": caesars_superdome,
            "16461": neo_quimica_arena,
            "29574": fedex_field,
            "16118": tottenham_hotspur_stadium,
            "16163": wembley_stadium,
            "15537": allianz_arena,
            "29573": levis_stadium,
            "3718": tom_bensom_hall_of_fame_stadium,
            "3738": gilette_stadium,
            "3673": lumen_field,
            "3874": paycor_stadium,
            "3727": ford_field,
            "3948": hard_rock_stadium,
            "3886": raymond_james_stadium,
            "3679": cleveland_browns_stadium,
            "3970": state_farm_stadium,
            "3883": highmark_stadium,
            "3933": soldier_field,
            "3628": bank_of_america_stadium,
            "3687": att_stadium,
            "3814": mtt_bank_stadium,
            "7065": sofi_stadium,
            "3493": caesars_superdome,
            "6501": allegiant_stadium,
            "3806": lincoln_financial_field,
            "3839": metlife_stadium,
            "5348": mercedez_benz_stadium,
            "3891": nrg_stadium,
            "3752": acrisure_stadium,
            "3812": lucas_oil_stadium,
            "3798": lambeau_field,
            "5239": us_bank_stadium,
            "4738": levis_stadium,
            "3719": fedex_field,
            "3810": nissan_stadium,
            "3622": arrowhead_stadium,
            "3712": everbank_stadium,
            "3937": empower_field,
            "15814": levis_stadium,
            "17590": deutsche_bank_park,
            "2455": wembley_stadium,
            "5534": tottenham_hotspur_stadium,
            "1875": deutsche_bank_park,
            "4013": camping_world_stadium,
            "1775": allianz_arena,
            "1850": estadio_azteca,
            "21629": arrowhead_stadium,
            "21607": paycor_stadium,
            "538": dignity_health_sports_park,
            "3867": oakland_coliseum,
            "477": los_angeles_memorial_coliseum,
            "5128": twickenham_stadium,
            "3495": georgia_dome,
            "3932": sdccu_stadium,
            "3494": trans_world_dome,
            "3953": us_bank_stadium,
            "3669": candlestick_park,
            "16": us_bank_stadium,
            "1822": rogers_centre,
            "3610": aloha_stadium,
            "3736": metlife_stadium,
            "3840": us_bank_stadium,
            "3954": texas_stadium,
            "50": empower_field,
            "24": candlestick_park,
            "3888": lucas_oil_stadium,
            "3947": mountain_america_stadium,
            "3977": lincoln_financial_field,
            "3929": silverdome,
            "28229": trans_world_dome,
            "30854": lumen_field,
            "15804": georgia_dome,
            "28181": caesars_superdome,
            "18214": metlife_stadium,
            "23380": empower_field,
            "18379": silverdome,
            "18383": gilette_stadium,
            "25758": lincoln_financial_field,
            "20450": texas_stadium,
            "20449": acrisure_stadium,
            "21559": sdccu_stadium,
            "21501": mountain_america_stadium,
            "3955": acrisure_stadium,
            "21515": liberty_bowl_memorial_stadium,
            "28192": nrg_stadium,
            "18381": rfk_stadium,
            "30845": paycor_stadium,
            "30853": candlestick_park,
            "30846": paycor_stadium,
            "20451": los_angeles_memorial_coliseum,
            "21572": vanderbilt_stadium,
            "16093": rose_bowl,
            "20447": miami_orange_bowl,
            "18382": stanford_stadium,
            "30850": milwaukee_county_stadium,
            "21813": shea_stadium,
            "20448": gilette_stadium,
            "21608": yale_bowl,
            "21532": tiger_stadium,
            "21581": war_memorial_stadium,
            "19474": yankee_stadium,
            "21642": municipal_stadium,
            "18378": cotton_bowl,
            "25773": kezar_stadium,
            "21659": franklin_field,
            "30763": wrigley_field,
            "19533": city_stadium,
            "4461": ig_field,
            "21557": rice_stadium,
            "3766": independence_stadium,
            "16280": memorial_stadium,
            "23848": shea_stadium,
            "17145": empower_field,
            "30856": att_stadium,
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
