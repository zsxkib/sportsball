"""Combined player model."""

# pylint: disable=too-many-locals
from ..player_model import PlayerModel


def create_combined_player_model(
    player_models: list[PlayerModel], identifier: str
) -> PlayerModel:
    """Create a player model by combining many player models."""
    jersey = None
    kicks = None
    fumbles = None
    fumbles_lost = None
    field_goals = None
    field_goals_attempted = None
    offensive_rebounds = None
    assists = None
    turnovers = None
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
        player_model_fumbles_lost = player_model.fumbles_lost
        if player_model_fumbles_lost is not None:
            fumbles_lost = player_model_fumbles_lost
        player_model_field_goals = player_model.field_goals
        if player_model_field_goals is not None:
            field_goals = player_model_field_goals
        player_model_field_goals_attempted = player_model.field_goals_attempted
        if player_model_field_goals_attempted is not None:
            field_goals_attempted = player_model_field_goals_attempted
        player_model_offensive_rebounds = player_model.offensive_rebounds
        if player_model_offensive_rebounds is not None:
            offensive_rebounds = player_model_offensive_rebounds
        player_model_assists = player_model.assists
        if player_model_assists is not None:
            assists = player_model_assists
        player_model_turnovers = player_model.turnovers
        if player_model_turnovers is not None:
            turnovers = player_model_turnovers
    return PlayerModel(
        identifier=identifier,
        jersey=jersey,
        kicks=kicks,
        fumbles=fumbles,
        fumbles_lost=fumbles_lost,
        field_goals=field_goals,
        field_goals_attempted=field_goals_attempted,
        offensive_rebounds=offensive_rebounds,
        assists=assists,
        turnovers=turnovers,
    )
