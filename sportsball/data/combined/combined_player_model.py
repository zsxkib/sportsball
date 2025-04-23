"""Combined player model."""

# pylint: disable=too-many-locals,too-many-branches,too-many-statements,duplicate-code
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
    name = None
    marks = None
    handballs = None
    disposals = None
    goals = None
    behinds = None
    hit_outs = None
    tackles = None
    rebounds = None
    insides = None
    clearances = None
    clangers = None
    free_kicks_for = None
    free_kicks_against = None
    brownlow_votes = None
    contested_possessions = None
    uncontested_possessions = None
    contested_marks = None
    marks_inside = None
    one_percenters = None
    bounces = None
    goal_assists = None
    percentage_played = None
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
        player_model_name = player_model.name
        if player_model_name is not None:
            name = player_model_name
        player_model_marks = player_model.marks
        if player_model_marks is not None:
            marks = player_model_marks
        player_model_handballs = player_model.handballs
        if player_model_handballs is not None:
            handballs = player_model_handballs
        player_model_disposals = player_model.disposals
        if player_model_disposals is not None:
            disposals = player_model_disposals
        player_model_goals = player_model.goals
        if player_model_goals is not None:
            goals = player_model_goals
        player_model_behinds = player_model.behinds
        if player_model_behinds is not None:
            behinds = player_model_behinds
        player_model_hit_outs = player_model.hit_outs
        if player_model_hit_outs is not None:
            hit_outs = player_model_hit_outs
        player_model_tackles = player_model.tackles
        if player_model_tackles is not None:
            tackles = player_model_tackles
        player_model_rebounds = player_model.rebounds
        if player_model_rebounds is not None:
            rebounds = player_model_rebounds
        player_model_insides = player_model.insides
        if player_model_insides is not None:
            insides = player_model_insides
        player_model_clearances = player_model.clearances
        if player_model_clearances is not None:
            clearances = player_model_clearances
        player_model_clangers = player_model.clangers
        if player_model_clangers is not None:
            clangers = player_model_clangers
        player_model_free_kicks_for = player_model.free_kicks_for
        if player_model_free_kicks_for is not None:
            free_kicks_for = player_model_free_kicks_for
        player_model_free_kicks_against = player_model.free_kicks_against
        if player_model_free_kicks_against is not None:
            free_kicks_against = player_model_free_kicks_against
        player_model_brownlow_votes = player_model.brownlow_votes
        if player_model_brownlow_votes is not None:
            brownlow_votes = player_model_brownlow_votes
        player_model_contested_possessions = player_model.contested_possessions
        if player_model_contested_possessions is not None:
            contested_possessions = player_model_contested_possessions
        player_model_uncontested_possessions = player_model.uncontested_possessions
        if player_model_uncontested_possessions is not None:
            uncontested_possessions = player_model_uncontested_possessions
        player_model_contested_marks = player_model.contested_marks
        if player_model_contested_marks is not None:
            contested_marks = player_model_contested_marks
        player_model_marks_inside = player_model.marks_inside
        if player_model_marks_inside is not None:
            marks_inside = player_model_marks_inside
        player_model_one_percenters = player_model.one_percenters
        if player_model_one_percenters is not None:
            one_percenters = player_model_one_percenters
        player_model_bounces = player_model.bounces
        if player_model_bounces is not None:
            bounces = player_model_bounces
        player_model_goal_assists = player_model.goal_assists
        if player_model_goal_assists is not None:
            goal_assists = player_model_goal_assists
        player_model_percentage_played = player_model.percentage_played
        if player_model_percentage_played is not None:
            percentage_played = player_model_percentage_played
    if name is None:
        raise ValueError("name is null.")
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
        name=name,
        marks=marks,
        handballs=handballs,
        disposals=disposals,
        goals=goals,
        behinds=behinds,
        hit_outs=hit_outs,
        tackles=tackles,
        rebounds=rebounds,
        insides=insides,
        clearances=clearances,
        clangers=clangers,
        free_kicks_for=free_kicks_for,
        free_kicks_against=free_kicks_against,
        brownlow_votes=brownlow_votes,
        contested_possessions=contested_possessions,
        uncontested_possessions=uncontested_possessions,
        contested_marks=contested_marks,
        marks_inside=marks_inside,
        one_percenters=one_percenters,
        bounces=bounces,
        goal_assists=goal_assists,
        percentage_played=percentage_played,
    )
