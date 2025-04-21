"""AFL AFL player model."""

from ...player_model import PlayerModel


def create_afl_afl_player_model(
    identifier: str,
    player_number: str,
    name: str,
) -> PlayerModel:
    """Create a player model from AFL AFL."""
    return PlayerModel(
        identifier=identifier,
        jersey=player_number,
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
    )
