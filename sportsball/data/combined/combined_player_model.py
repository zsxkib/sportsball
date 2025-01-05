"""Combined player model."""

from ..player_model import PlayerModel


def create_combined_player_model(
    player_models: list[PlayerModel], identifier: str
) -> PlayerModel:
    """Create a player model by combining many player models."""
    jersey = None
    kicks = None
    fumbles = None
    for player_model in player_models:
        player_model_jersey = player_model.jersey
        if player_model_jersey is not None:
            jersey = player_model_jersey
        player_model_kicks = player_model.kicks
        if player_model_kicks is not None:
            kicks = player_model_kicks
        player_model_fumbles = player_model.fumbles
        if player_model_fumbles is not None:
            fumbles = player_model_fumbles
    return PlayerModel(
        identifier=identifier, jersey=jersey, kicks=kicks, fumbles=fumbles
    )
