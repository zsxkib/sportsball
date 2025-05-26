"""HKJC HKJC player model."""

# pylint: disable=too-many-arguments
import pytest_is_running

from ....cache import MEMORY
from ...player_model import PlayerModel
from ...sex import Sex
from ...species import Species
from ..position import Position


def _create_hkjc_hkjc_player_model(
    species: Species,
    name: str,
    handicap_weight: float | None,
    father: PlayerModel | None,
    sex: Sex | None,
    age: int | None,
    starting_position: Position | None,
) -> PlayerModel:
    return PlayerModel(
        identifier=name,
        jersey=None,
        kicks=None,
        fumbles=None,
        fumbles_lost=None,
        field_goals=None,
        field_goals_attempted=None,
        offensive_rebounds=None,
        assists=None,
        turnovers=None,
        name=name,
        marks=None,
        handballs=None,
        disposals=None,
        goals=None,
        behinds=None,
        hit_outs=None,
        tackles=None,
        rebounds=None,
        insides=None,
        clearances=None,
        clangers=None,
        free_kicks_for=None,
        free_kicks_against=None,
        brownlow_votes=None,
        contested_possessions=None,
        uncontested_possessions=None,
        contested_marks=None,
        marks_inside=None,
        one_percenters=None,
        bounces=None,
        goal_assists=None,
        percentage_played=None,
        birth_date=None,
        species=str(species),
        handicap_weight=handicap_weight,
        father=father,
        sex=str(sex) if sex is not None else None,
        age=age,
        starting_position=str(starting_position)
        if starting_position is not None
        else None,
    )


@MEMORY.cache
def _cached_create_hkjc_hkjc_player_model(
    species: Species,
    name: str,
    handicap_weight: float | None,
    father: PlayerModel | None,
    sex: Sex | None,
    age: int | None,
    starting_position: Position | None,
) -> PlayerModel:
    return _create_hkjc_hkjc_player_model(
        species, name, handicap_weight, father, sex, age, starting_position
    )


def create_hkjc_hkjc_player_model(
    species: Species,
    name: str,
    handicap_weight: float | None,
    father: PlayerModel | None,
    sex: Sex | None,
    age: int | None,
    starting_position: Position | None,
) -> PlayerModel:
    """Create a player model based off HKJC."""
    if not pytest_is_running.is_running():
        return _cached_create_hkjc_hkjc_player_model(
            species, name, handicap_weight, father, sex, age, starting_position
        )
    return _create_hkjc_hkjc_player_model(
        species, name, handicap_weight, father, sex, age, starting_position
    )
