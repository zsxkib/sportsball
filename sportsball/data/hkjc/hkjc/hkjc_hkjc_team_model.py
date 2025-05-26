"""HKJC HKJC team model."""

from typing import Any

import pytest_is_running

from ....cache import MEMORY
from ...sex import Sex
from ...species import Species
from ...team_model import TeamModel
from ..position import position_from_str
from .hkjc_hkjc_coach_model import create_hkjc_hkjc_coach_model
from .hkjc_hkjc_player_model import create_hkjc_hkjc_player_model

SIRE_KEY = "sire"


def _create_hkjc_hkjc_team_model(
    runner: dict[str, Any],
    racers: int,
) -> TeamModel:
    def sex_code_to_sex(sex_code: str) -> Sex:
        sex_code = sex_code.lower()
        if sex_code == "g":
            return Sex.GELDING
        if sex_code == "h":
            return Sex.STALLION
        if sex_code == "f":
            return Sex.FILLY
        if sex_code == "m":
            return Sex.MARE
        if sex_code == "c":
            return Sex.COLT
        if sex_code == "r":
            return Sex.RIG
        raise ValueError(f"Unrecognised sex code: {sex_code}")

    sire_player = create_hkjc_hkjc_player_model(
        Species.HORSE, runner[SIRE_KEY], None, None, Sex.STALLION, None, None
    )
    position = str(runner["barrierDrawNumber"]).strip()
    players = [
        create_hkjc_hkjc_player_model(
            Species.HORSE,
            runner["horse"]["name_en"],
            float(runner["handicapWeight"]) / 2.2,
            sire_player,
            sex_code_to_sex(runner["sexNm"]["english"]),
            runner["age"],
            position_from_str(position) if position else None,
        ),
        create_hkjc_hkjc_player_model(
            Species.HUMAN,
            runner["jockey"]["name_en"],
            None,
            None,
            None,
            None,
            None,
        ),
    ]
    coach = create_hkjc_hkjc_coach_model(runner["trainer"]["name_en"])
    name = " - ".join([x.name for x in players])
    location = runner["horse"]["name_en"].split("(")[1].replace(")", "").strip()
    points = float(racers - runner["finalPosition"])
    return TeamModel(
        identifier=name,
        name=name,
        location=location,
        players=players,
        odds=[],
        points=points,
        ladder_rank=None,
        news=[],
        social=[],
        field_goals=None,
        coaches=[coach],
    )


@MEMORY.cache
def _cached_create_hkjc_hkjc_team_model(
    runner: dict[str, Any],
    racers: int,
) -> TeamModel:
    return _create_hkjc_hkjc_team_model(runner, racers)


def create_hkjc_hkjc_team_model(
    runner: dict[str, Any],
    racers: int,
) -> TeamModel:
    """Create team model from HKJC."""
    if not pytest_is_running.is_running():
        return _cached_create_hkjc_hkjc_team_model(runner, racers)
    return _create_hkjc_hkjc_team_model(runner, racers)
