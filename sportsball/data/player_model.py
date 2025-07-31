"""The prototype class for a player."""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from .address_model import VERSION as ADDRESS_VERSION
from .address_model import AddressModel
from .delimiter import DELIMITER
from .field_type import FFILL_KEY, TYPE_KEY, FieldType
from .owner_model import VERSION as OWNER_VERSION
from .owner_model import OwnerModel
from .sex import (FEMALE_GENDERS, GENDER_DETECTOR, MALE_GENDERS,
                  UNCERTAIN_GENDERS, Sex)
from .venue_model import VERSION as VENUE_VERSION
from .venue_model import VenueModel

PLAYER_KICKS_COLUMN: Literal["kicks"] = "kicks"
PLAYER_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
PLAYER_FUMBLES_COLUMN: Literal["fumbles"] = "fumbles"
PLAYER_FUMBLES_LOST_COLUMN: Literal["fumbles_lost"] = "fumbles_lost"
FIELD_GOALS_COLUMN: Literal["field_goals"] = "field_goals"
FIELD_GOALS_ATTEMPTED_COLUMN: Literal["field_goals_attempted"] = "field_goals_attempted"
OFFENSIVE_REBOUNDS_COLUMN: Literal["offensive_rebounds"] = "offensive_rebounds"
PLAYER_ASSISTS_COLUMN: Literal["assists"] = "assists"
TURNOVERS_COLUMN: Literal["turnovers"] = "turnovers"
PLAYER_MARKS_COLUMN: Literal["marks"] = "marks"
PLAYER_HANDBALLS_COLUMN: Literal["handballs"] = "handballs"
PLAYER_DISPOSALS_COLUMN: Literal["disposals"] = "disposals"
PLAYER_GOALS_COLUMN: Literal["goals"] = "goals"
PLAYER_BEHINDS_COLUMN: Literal["behinds"] = "behinds"
PLAYER_HIT_OUTS_COLUMN: Literal["hit_outs"] = "hit_outs"
PLAYER_TACKLES_COLUMN: Literal["tackles"] = "tackles"
PLAYER_REBOUNDS_COLUMN: Literal["rebounds"] = "rebounds"
PLAYER_INSIDES_COLUMN: Literal["insides"] = "insides"
PLAYER_CLEARANCES_COLUMN: Literal["clearances"] = "clearances"
PLAYER_CLANGERS_COLUMN: Literal["clangers"] = "clangers"
PLAYER_FREE_KICKS_FOR_COLUMN: Literal["free_kicks_for"] = "free_kicks_for"
PLAYER_FREE_KICKS_AGAINST_COLUMN: Literal["free_kicks_against"] = "free_kicks_against"
PLAYER_BROWNLOW_VOTES_COLUMN: Literal["brownlow_votes"] = "brownlow_votes"
PLAYER_CONTESTED_POSSESSIONS_COLUMN: Literal["contested_possessions"] = (
    "contested_possessions"
)
PLAYER_UNCONTESTED_POSSESSIONS_COLUMN: Literal["uncontested_possessions"] = (
    "uncontested_possessions"
)
PLAYER_CONTESTED_MARKS_COLUMN: Literal["contested_marks"] = "contested_marks"
PLAYER_MARKS_INSIDE_COLUMN: Literal["marks_inside"] = "marks_inside"
PLAYER_ONE_PERCENTERS_COLUMN: Literal["one_percenters"] = "one_percenters"
PLAYER_BOUNCES_COLUMN: Literal["bounces"] = "bounces"
PLAYER_GOAL_ASSISTS_COLUMN: Literal["goal_assists"] = "goal_assists"
PLAYER_PERCENTAGE_PLAYED_COLUMN: Literal["percentage_played"] = "percentage_played"
PLAYER_NAME_COLUMN: Literal["name"] = "name"
PLAYER_BIRTH_DATE_COLUMN: Literal["birth_date"] = "birth_date"
PLAYER_SPECIES_COLUMN: Literal["species"] = "species"
PLAYER_HANDICAP_WEIGHT_COLUMN: Literal["handicap_weight"] = "handicap_weight"
PLAYER_FATHER_COLUMN: Literal["father"] = "father"
PLAYER_SEX_COLUMN: Literal["sex"] = "sex"
PLAYER_AGE_COLUMN: Literal["age"] = "age"
PLAYER_STARTING_POSITION_COLUMN: Literal["starting_position"] = "starting_position"
PLAYER_WEIGHT_COLUMN: Literal["weight"] = "weight"
PLAYER_BIRTH_ADDRESS_COLUMN: Literal["birth_address"] = "birth_address"
PLAYER_OWNER_COLUMN: Literal["owner"] = "owner"
PLAYER_SECONDS_PLAYED_COLUMN: Literal["seconds_played"] = "seconds_played"
PLAYER_FIELD_GOALS_PERCENTAGE_COLUMN: Literal["field_goals_percentage"] = (
    "field_goals_percentage"
)
PLAYER_THREE_POINT_FIELD_GOALS_COLUMN: Literal["three_point_field_goals"] = (
    "three_point_field_goals"
)
PLAYER_THREE_POINT_FIELD_GOALS_ATTEMPTED_COLUMN: Literal[
    "three_point_field_goals_attempted"
] = "three_point_field_goals_attempted"
PLAYER_THREE_POINT_FIELD_GOALS_PERCENTAGE_COLUMN: Literal[
    "three_point_field_goals_percentage"
] = "three_point_field_goals_percentage"
PLAYER_FREE_THROWS_COLUMN: Literal["free_throws"] = "free_throws"
PLAYER_FREE_THROWS_ATTEMPTED_COLUMN: Literal["free_throws_attempted"] = (
    "free_throws_attempted"
)
PLAYER_FREE_THROWS_PERCENTAGE_COLUMN: Literal["free_throws_percentage"] = (
    "free_throws_percentage"
)
PLAYER_DEFENSIVE_REBOUNDS_COLUMN: Literal["defensive_rebounds"] = "defensive_rebounds"
PLAYER_TOTAL_REBOUNDS_COLUMN: Literal["total_rebounds"] = "total_rebounds"
PLAYER_STEALS_COLUMN: Literal["steals"] = "steals"
PLAYER_BLOCKS_COLUMN: Literal["blocks"] = "blocks"
PLAYER_PERSONAL_FOULS_COLUMN: Literal["personal_fouls"] = "personal_fouls"
PLAYER_POINTS_COLUMN: Literal["points"] = "points"
PLAYER_GAME_SCORE_COLUMN: Literal["game_score"] = "game_score"
PLAYER_POINT_DIFFERENTIAL_COLUMN: Literal["point_differential"] = "point_differential"
PLAYER_HEIGHT_COLUMN: Literal["height"] = "height"
PLAYER_COLLEGES_COLUMN: Literal["colleges"] = "colleges"
PLAYER_HEADSHOT_COLUMN: Literal["headshot"] = "headshot"
PLAYER_FORCED_FUMBLES_COLUMN: Literal["forced_fumbles"] = "forced_fumbles"
PLAYER_FUMBLES_RECOVERED_COLUMN: Literal["fumbles_recovered"] = "fumbles_recovered"
PLAYER_FUMBLES_RECOVERED_YARDS_COLUMN: Literal["fumbles_recovered_yards"] = (
    "fumbles_recovered_yards"
)
PLAYER_FUMBLES_TOUCHDOWNS_COLUMN: Literal["fumbles_touchdowns"] = "fumbles_touchdowns"
PLAYER_OFFENSIVE_TWO_POINT_RETURNS_COLUMN: Literal["offensive_two_point_returns"] = (
    "offensive_two_point_returns"
)
PLAYER_OFFENSIVE_FUMBLES_TOUCHDOWNS_COLUMN: Literal["offensive_fumbles_touchdowns"] = (
    "offensive_fumbles_touchdowns"
)
PLAYER_DEFENSIVE_FUMBLES_TOUCHDOWNS_COLUMN: Literal["defensive_fumbles_touchdowns"] = (
    "defensive_fumbles_touchdowns"
)
PLAYER_AVERAGE_GAIN_COLUMN: Literal["average_gain"] = "average_gain"
PLAYER_COMPLETION_PERCENTAGE_COLUMN: Literal["completion_percentage"] = (
    "completion_percentage"
)
PLAYER_COMPLETIONS_COLUMN: Literal["completions"] = "completions"
PLAYER_ESPN_QUARTERBACK_RATING_COLUMN: Literal["espn_quarterback_rating"] = (
    "espn_quarterback_rating"
)
PLAYER_INTERCEPTION_PERCENTAGE_COLUMN: Literal["interception_percentage"] = (
    "interception_percentage"
)
PLAYER_INTERCEPTIONS_COLUMN: Literal["interceptions"] = "interceptions"
PLAYER_LONG_PASSING_COLUMN: Literal["long_passing"] = "long_passing"
PLAYER_MISC_YARDS_COLUMN: Literal["misc_yards"] = "misc_yards"
PLAYER_NET_PASSING_YARDS_COLUMN: Literal["net_passing_yards"] = "net_passing_yards"
PLAYER_NET_TOTAL_YARDS_COLUMN: Literal["net_total_yards"] = "net_total_yards"
PLAYER_PASSING_ATTEMPTS_COLUMN: Literal["passing_attempts"] = "passing_attempts"
PLAYER_PASSING_BIG_PLAYS_COLUMN: Literal["passing_big_plays"] = "passing_big_plays"
PLAYER_PASSING_FIRST_DOWNS_COLUMN: Literal["passing_first_downs"] = (
    "passing_first_downs"
)
PLAYER_PASSING_FUMBLES_COLUMN: Literal["passing_fumbles"] = "passing_fumbles"
PLAYER_PASSING_FUMBLES_LOST_COLUMN: Literal["passing_fumbles_lost"] = (
    "passing_fumbles_lost"
)
PLAYER_PASSING_TOUCHDOWN_PERCENTAGE_COLUMN: Literal["passing_touchdown_percentage"] = (
    "passing_touchdown_percentage"
)
PLAYER_PASSING_TOUCHDOWNS_COLUMN: Literal["passing_touchdowns"] = "passing_touchdowns"
PLAYER_PASSING_YARDS_COLUMN: Literal["passing_yards"] = "passing_yards"
PLAYER_PASSING_YARDS_AFTER_CATCH_COLUMN: Literal["passing_yards_after_catch"] = (
    "passing_yards_after_catch"
)
PLAYER_PASSING_YARDS_AT_CATCH_COLUMN: Literal["passing_yards_at_catch"] = (
    "passing_yards_at_catch"
)
PLAYER_QUARTERBACK_RATING_COLUMN: Literal["quarterback_rating"] = "quarterback_rating"
PLAYER_SACKS_COLUMN: Literal["sacks"] = "sacks"
PLAYER_SACKS_YARDS_LOST_COLUMN: Literal["sacks_yards_lost"] = "sacks_yards_lost"
PLAYER_NET_PASSING_ATTEMPTS_COLUMN: Literal["net_passing_attempts"] = (
    "net_passing_attempts"
)
PLAYER_TOTAL_OFFENSIVE_PLAYS_COLUMN: Literal["total_offensive_plays"] = (
    "total_offensive_plays"
)
PLAYER_TOTAL_POINTS_COLUMN: Literal["total_points"] = "total_points"
PLAYER_TOTAL_TOUCHDOWNS_COLUMN: Literal["total_touchdowns"] = "total_touchdowns"
PLAYER_TOTAL_YARDS_COLUMN: Literal["total_yards"] = "total_yards"
PLAYER_TOTAL_YARDS_FROM_SCRIMMAGE_COLUMN: Literal["total_yards_from_scrimmage"] = (
    "total_yards_from_scrimmage"
)
PLAYER_TWO_POINT_PASS_COLUMN: Literal["two_point_pass"] = "two_point_pass"
PLAYER_TWO_POINT_PASS_ATTEMPT_COLUMN: Literal["two_point_pass_attempt"] = (
    "two_point_pass_attempt"
)
PLAYER_YARDS_PER_COMPLETION_COLUMN: Literal["yards_per_completion"] = (
    "yards_per_completion"
)
PLAYER_YARDS_PER_PASS_ATTEMPT_COLUMN: Literal["yards_per_pass_attempt"] = (
    "yards_per_pass_attempt"
)
PLAYER_NET_YARDS_PER_PASS_ATTEMPT_COLUMN: Literal["net_yards_per_pass_attempt"] = (
    "net_yards_per_pass_attempt"
)
PLAYER_ESPN_RUNNINGBACK_RATING_COLUMN: Literal["espn_runningback"] = "espn_runningback"
PLAYER_LONG_RUSHING_COLUMN: Literal["long_rushing"] = "long_rushing"
PLAYER_RUSHING_ATTEMPTS_COLUMN: Literal["rushing_attempts"] = "rushing_attempts"
PLAYER_RUSHING_BIG_PLAYS_COLUMN: Literal["rushing_big_plays"] = "rushing_big_plays"
PLAYER_RUSHING_FIRST_DOWNS_COLUMN: Literal["rushing_first_downs"] = (
    "rushing_first_downs"
)
PLAYER_RUSHING_FUMBLES_COLUMN: Literal["rushing_fumbles"] = "rushing_fumbles"
PLAYER_RUSHING_FUMBLES_LOST_COLUMN: Literal["rushing_fumbles_lost"] = (
    "rushing_fumbles_lost"
)
PLAYER_RUSHING_TOUCHDOWNS_COLUMN: Literal["rushing_touchdowns"] = "rushing_touchdowns"
PLAYER_RUSHING_YARDS_COLUMN: Literal["rushing_yards"] = "rushing_yards"
PLAYER_STUFFS_COLUMN: Literal["stuffs"] = "stuffs"
PLAYER_STUFF_YARDS_LOST: Literal["stuff_yards_lost"] = "stuff_yards_lost"
PLAYER_TWO_POINT_RUSH_COLUMN: Literal["two_point_rush"] = "two_point_rush"
PLAYER_TWO_POINT_RUSH_ATTEMPTS_COLUMN: Literal["two_point_rush_attempts"] = (
    "two_point_rush_attempts"
)
PLAYER_YARDS_PER_RUSH_ATTEMPT_COLUMN: Literal["yards_per_rush_attempt"] = (
    "yards_per_rush_attempt"
)
PLAYER_ESPN_WIDERECEIVER_COLUMN: Literal["espn_widereceiver"] = "espn_widereceiver"
PLAYER_LONG_RECEPTION_COLUMN: Literal["long_reception"] = "long_reception"
PLAYER_RECEIVING_BIG_PLAYS_COLUMN: Literal["receiving_big_plays"] = (
    "receiving_big_plays"
)
PLAYER_RECEIVING_FIRST_DOWNS_COLUMN: Literal["receiving_first_downs"] = (
    "receiving_first_downs"
)
PLAYER_RECEIVING_FUMBLES_COLUMN: Literal["receiving_fumbles"] = "receiving_fumbles"
PLAYER_RECEIVING_FUMBLES_LOST_COLUMN: Literal["receiving_fumbles_lost"] = (
    "receiving_fumbles_lost"
)
PLAYER_RECEIVING_TARGETS_COLUMN: Literal["receiving_targets"] = "receiving_targets"
PLAYER_RECEIVING_TOUCHDOWNS_COLUMN: Literal["receiving_touchdowns"] = (
    "receiving_touchdowns"
)
PLAYER_RECEIVING_YARDS_COLUMN: Literal["receiving_yards"] = "receiving_yards"
PLAYER_RECEIVING_YARDS_AFTER_CATCH_COLUMN: Literal["receiving_yards_after_catch"] = (
    "receiving_yards_after_catch"
)
PLAYER_RECEIVING_YARDS_AT_CATCH_COLUMN: Literal["receiving_yards_at_catch"] = (
    "receiving_yards_at_catch"
)
PLAYER_RECEPTIONS_COLUMN: Literal["receptions"] = "receptions"
PLAYER_TWO_POINT_RECEPTIONS_COLUMN: Literal["two_point_receptions"] = (
    "two_point_receptions"
)
PLAYER_TWO_POINT_RECEPTION_ATTEMPTS_COLUMN: Literal["two_point_reception_attempts"] = (
    "two_point_reception_attempts"
)
PLAYER_YARDS_PER_RECEPTION_COLUMN: Literal["yards_per_reception"] = (
    "yards_per_reception"
)
PLAYER_ASSIST_TACKLES_COLUMN: Literal["assist_tackles"] = "assist_tackles"
PLAYER_AVERAGE_INTERCEPTION_YARDS_COLUMN: Literal["average_interception_yards"] = (
    "average_interception_yards"
)
PLAYER_AVERAGE_SACK_YARDS_COLUMN: Literal["average_sack_yards"] = "average_sack_yards"
PLAYER_AVERAGE_STUFF_YARDS_COLUMN: Literal["average_stuff_yards"] = (
    "average_stuff_yards"
)
PLAYER_BLOCKED_FIELD_GOAL_TOUCHDOWNS_COLUMN: Literal[
    "blocked_field_goal_touchdowns"
] = "blocked_field_goal_touchdowns"
PLAYER_BLOCKED_PUNT_TOUCHDOWNS_COLUMN: Literal["blocked_punt_touchdowns"] = (
    "blocked_punt_touchdowns"
)
PLAYER_DEFENSIVE_TOUCHDOWNS_COLUMN: Literal["defensive_touchdowns"] = (
    "defensive_touchdowns"
)
PLAYER_HURRIES_COLUMN: Literal["hurries"] = "hurries"
PLAYER_KICKS_BLOCKED_COLUMN: Literal["kicks_blocked"] = "kicks_blocked"
PLAYER_LONG_INTERCEPTION_COLUMN: Literal["long_interception"] = "long_interception"
PLAYER_MISC_TOUCHDOWNS_COLUMN: Literal["misc_touchdowns"] = "misc_touchdowns"
PLAYER_PASSES_BATTED_DOWN_COLUMN: Literal["passes_batted_down"] = "passes_batted_down"
PLAYER_PASSES_DEFENDED_COLUMN: Literal["passes_defended"] = "passes_defended"
PLAYER_QUARTERBACK_HITS_COLUMN: Literal["quarterback_hits"] = "quarterback_hits"
PLAYER_SACKS_ASSISTED_COLUMN: Literal["sacks_assisted"] = "sacks_assisted"
PLAYER_SACKS_UNASSISTED_COLUMN: Literal["sacks_unassisted"] = "sacks_unassisted"
PLAYER_SACKS_YARDS_COLUMN: Literal["sacks_yards"] = "sacks_yards"
PLAYER_SAFETIES_COLUMN: Literal["safeties"] = "safeties"
PLAYER_SOLO_TACKLES_COLUMN: Literal["solo_tackles"] = "solo_tackles"
PLAYER_STUFF_YARDS_COLUMN: Literal["stuff_yards"] = "stuff_yards"
PLAYER_TACKLES_FOR_LOSS_COLUMN: Literal["tackles_for_loss"] = "tackles_for_loss"
PLAYER_TACKLES_YARDS_LOST_COLUMN: Literal["tackles_yards_lost"] = "tackles_yards_lost"
PLAYER_YARDS_ALLOWED_COLUMN: Literal["yards_allowed"] = "yards_allowed"
PLAYER_POINTS_ALLOWED_COLUMN: Literal["points_allowed"] = "points_allowed"
PLAYER_ONE_POINT_SAFETIES_MADE_COLUMN: Literal["one_point_safeties_made"] = (
    "one_point_safeties_made"
)
PLAYER_MISSED_FIELD_GOAL_RETURN_TD_COLUMN: Literal["missed_field_goal_return_td"] = (
    "missed_field_goal_return_td"
)
PLAYER_BLOCKED_PUNT_EZ_REC_TD_COLUMN: Literal["blocked_punt_ez_rec_td"] = (
    "blocked_punt_ez_rec_td"
)
PLAYER_INTERCEPTION_TOUCHDOWNS_COLUMN: Literal["interception_touchdowns"] = (
    "interception_touchdowns"
)
PLAYER_INTERCEPTION_YARDS_COLUMN: Literal["interception_yards"] = "interception_yards"
PLAYER_AVERAGE_KICKOFF_RETURN_YARDS_COLUMN: Literal["average_kickoff_return_yards"] = (
    "average_kickoff_return_yards"
)
PLAYER_AVERAGE_KICKOFF_YARDS_COLUMN: Literal["average_kickoff_yards"] = (
    "average_kickoff_yards"
)
PLAYER_EXTRA_POINT_ATTEMPTS_COLUMN: Literal["extra_point_attempts"] = (
    "extra_point_attempts"
)
PLAYER_EXTRA_POINT_PERCENTAGE_COLUMN: Literal["extra_point_percentage"] = (
    "extra_point_percentage"
)
PLAYER_EXTRA_POINT_BLOCKED_COLUMN: Literal["extra_point_blocked"] = (
    "extra_point_blocked"
)
PLAYER_EXTRA_POINTS_BLOCKED_PERCENTAGE_COLUMN: Literal[
    "extra_points_blocked_percentage"
] = "extra_points_blocked_percentage"
PLAYER_EXTRA_POINTS_MADE_COLUMN: Literal["extra_points_made"] = "extra_points_made"
PLAYER_FAIR_CATCHES_COLUMN: Literal["fair_catches"] = "fair_catches"
PLAYER_FAIR_CATCH_PERCENTAGE_COLUMN: Literal["fair_catch_percentage"] = (
    "fair_catch_percentage"
)
PLAYER_FIELD_GOAL_ATTEMPTS_MAX_19_YARDS_COLUMN: Literal[
    "field_goal_attempts_max_19_yards"
] = "field_goal_attempts_max_19_yards"
PLAYER_FIELD_GOAL_ATTEMPTS_MAX_29_YARDS_COLUMN: Literal[
    "field_goal_attempts_max_29_yards"
] = "field_goal_attempts_max_29_yards"
PLAYER_FIELD_GOAL_ATTEMPTS_MAX_39_YARDS_COLUMN: Literal[
    "field_goal_attempts_max_39_yards"
] = "field_goal_attempts_max_39_yards"
PLAYER_FIELD_GOAL_ATTEMPTS_MAX_49_YARDS_COLUMN: Literal[
    "field_goal_attempts_max_49_yards"
] = "field_goal_attempts_max_49_yards"
PLAYER_FIELD_GOAL_ATTEMPTS_MAX_59_YARDS_COLUMN: Literal[
    "field_goal_attempts_max_59_yards"
] = "field_goal_attempts_max_59_yards"
PLAYER_FIELD_GOAL_ATTEMPTS_MAX_99_YARDS_COLUMN: Literal[
    "field_goal_attempts_max_99_yards"
] = "field_goal_attempts_max_99_yards"
PLAYER_FIELD_GOAL_ATTEMPTS_ABOVE_50_YARDS_COLUMN: Literal[
    "field_goal_attempts_above_50_yards"
] = "field_goal_attempts_above_50_yards"
PLAYER_FIELD_GOAL_ATTEMPT_YARDS_COLUMN: Literal["field_goal_attempt_yards"] = (
    "field_goal_attempt_yards"
)
PLAYER_FIELD_GOALS_BLOCKED_COLUMN: Literal["field_goals_blocked"] = (
    "field_goals_blocked"
)
PLAYER_FIELD_GOALS_BLOCKED_PERCENTAGE_COLUMN: Literal[
    "field_goals_blocked_percentage"
] = "field_goals_blocked_percentage"
PLAYER_FIELD_GOALS_MADE_COLUMN: Literal["field_goals_made"] = "field_goals_made"
PLAYER_FIELD_GOALS_MADE_MAX_19_YARDS_COLUMN: Literal[
    "field_goals_made_max_19_yards"
] = "field_goals_made_max_19_yards"
PLAYER_FIELD_GOALS_MADE_MAX_29_YARDS_COLUMN: Literal[
    "field_goals_made_max_29_yards"
] = "field_goals_made_max_29_yards"
PLAYER_FIELD_GOALS_MADE_MAX_39_YARDS_COLUMN: Literal[
    "field_goals_made_max_39_yards"
] = "field_goals_made_max_39_yards"
PLAYER_FIELD_GOALS_MADE_MAX_49_YARDS_COLUMN: Literal[
    "field_goals_made_max_49_yards"
] = "field_goals_made_max_49_yards"
PLAYER_FIELD_GOALS_MADE_MAX_59_YARDS_COLUMN: Literal[
    "field_goals_made_max_59_yards"
] = "field_goals_made_max_59_yards"
PLAYER_FIELD_GOALS_MADE_MAX_99_YARDS_COLUMN: Literal[
    "field_goals_made_max_99_yards"
] = "field_goals_made_max_99_yards"
PLAYER_FIELD_GOALS_MADE_ABOVE_50_YARDS_COLUMN: Literal[
    "field_goals_made_above_50_yards"
] = "field_goals_made_above_50_yards"
PLAYER_FIELD_GOALS_MADE_YARDS_COLUMN: Literal["field_goals_made_yards"] = (
    "field_goals_made_yards"
)
PLAYER_FIELD_GOALS_MISSED_YARDS_COLUMN: Literal["field_goals_missed_yards"] = (
    "field_goals_missed_yards"
)
PLAYER_KICKOFF_OUT_OF_BOUNDS_COLUMN: Literal["kickoff_out_of_bounds"] = (
    "kickoff_out_of_bounds"
)
PLAYER_KICKOFF_RETURNS_COLUMN: Literal["kickoff_returns"] = "kickoff_returns"
PLAYER_KICKOFF_RETURNS_TOUCHDOWNS_COLUMN: Literal["kickoff_returns_touchdowns"] = (
    "kickoff_returns_touchdowns"
)
PLAYER_KICKOFF_RETURN_YARDS_COLUMN: Literal["kickoff_return_yards"] = (
    "kickoff_return_yards"
)
PLAYER_KICKOFFS_COLUMN: Literal["kickoffs"] = "kickoffs"
PLAYER_KICKOFF_YARDS_COLUMN: Literal["kickoff_yards"] = "kickoff_yards"
PLAYER_LONG_FIELD_GOAL_ATTEMPT_COLUMN: Literal["long_field_goal_attempt"] = (
    "long_field_goal_attempt"
)
PLAYER_LONG_FIELD_GOAL_MADE_COLUMN: Literal["long_field_goal_made"] = (
    "long_field_goal_made"
)
PLAYER_LONG_KICKOFF_COLUMN: Literal["long_kickoff"] = "long_kickoff"
PLAYER_TOTAL_KICKING_POINTS_COLUMN: Literal["total_kicking_points"] = (
    "total_kicking_points"
)
PLAYER_TOUCHBACK_PERCENTAGE_COLUMN: Literal["touchback_percentage"] = (
    "touchback_percentage"
)
PLAYER_TOUCHBACKS_COLUMN: Literal["touchbacks"] = "touchbacks"
PLAYER_DEFENSIVE_FUMBLE_RETURNS_COLUMN: Literal["defensive_fumble_returns"] = (
    "defensive_fumble_returns"
)
PLAYER_DEFENSIVE_FUMBLE_RETURN_YARDS_COLUMN: Literal[
    "defensive_fumble_return_yards"
] = "defensive_fumble_return_yards"
PLAYER_FUMBLE_RECOVERIES_COLUMN: Literal["fumble_recoveries"] = "fumble_recoveries"
PLAYER_FUMBLE_RECOVERY_YARDS_COLUMN: Literal["fumble_recovery_yards"] = (
    "fumble_recovery_yards"
)
PLAYER_KICK_RETURN_FAIR_CATCHES_COLUMN: Literal["kick_return_fair_catches"] = (
    "kick_return_fair_catches"
)
PLAYER_KICK_RETURN_FAIR_CATCH_PERCENTAGE_COLUMN: Literal[
    "kick_return_fair_catch_percentage"
] = "kick_return_fair_catch_percentage"
PLAYER_KICK_RETURN_FUMBLES_COLUMN: Literal["kick_return_fumbles"] = (
    "kick_return_fumbles"
)
PLAYER_KICK_RETURN_FUMBLES_LOST_COLUMN: Literal["kick_return_fumbles_lost"] = (
    "kick_return_fumbles_lost"
)
PLAYER_KICK_RETURNS_COLUMN: Literal["kick_returns"] = "kick_returns"
PLAYER_KICK_RETURN_TOUCHDOWNS_COLUMN: Literal["kick_return_touchdowns"] = (
    "kick_return_touchdowns"
)
PLAYER_KICK_RETURN_YARDS_COLUMN: Literal["kick_return_yards"] = "kick_return_yards"
PLAYER_LONG_KICK_RETURN_COLUMN: Literal["long_kick_return"] = "long_kick_return"
PLAYER_LONG_PUNT_RETURN_COLUMN: Literal["long_punt_return"] = "long_punt_return"
PLAYER_MISC_FUMBLE_RETURNS_COLUMN: Literal["misc_fumble_returns"] = (
    "misc_fumble_returns"
)
PLAYER_MISC_FUMBLE_RETURN_YARDS_COLUMN: Literal["misc_fumble_return_yards"] = (
    "misc_fumble_return_yards"
)
PLAYER_OPPOSITION_FUMBLE_RECOVERIES_COLUMN: Literal["opposition_fumble_recoveries"] = (
    "opposition_fumble_recoveries"
)
PLAYER_OPPOSITION_FUMBLE_RECOVERY_YARDS_COLUMN: Literal[
    "opposition_fumble_recovery_yards"
] = "opposition_fumble_recovery_yards"
PLAYER_OPPOSITION_SPECIAL_TEAM_FUMBLE_RETURNS_COLUMN: Literal[
    "opposition_special_team_fumble_returns"
] = "opposition_special_team_fumble_returns"
PLAYER_OPPOSITION_SPECIAL_TEAM_FUMBLE_RETURN_YARDS_COLUMN: Literal[
    "opposition_special_team_fumble_return_yards"
] = "opposition_special_team_fumble_return_yards"
PLAYER_PUNT_RETURN_FAIR_CATCHES_COLUMN: Literal["punt_return_fair_catches"] = (
    "punt_return_fair_catches"
)
PLAYER_PUNT_RETURN_FAIR_CATCH_PERCENTAGE_COLUMN: Literal[
    "punt_return_fair_catch_percentage"
] = "punt_return_fair_catch_percentage"
PLAYER_PUNT_RETURN_FUMBLES_COLUMN: Literal["punt_return_fumbles"] = (
    "punt_return_fumbles"
)
PLAYER_PUNT_RETURN_FUMBLES_LOST_COLUMN: Literal["punt_return_fumbles_lost"] = (
    "punt_return_fumbles_lost"
)
PLAYER_PUNT_RETURNS_COLUMN: Literal["punt_returns"] = "punt_returns"
PLAYER_PUNT_RETURNS_STARTED_INSIDE_THE_10_COLUMN: Literal[
    "punt_returns_started_inside_the_10"
] = "punt_returns_started_inside_the_10"
PLAYER_PUNT_RETURNS_STARTED_INSIDE_THE_20_COLUMN: Literal[
    "punt_returns_started_inside_the_20"
] = "punt_returns_started_inside_the_20"
PLAYER_PUNT_RETURN_TOUCHDOWNS_COLUMN: Literal["punt_return_touchdowns"] = (
    "punt_return_touchdowns"
)
PLAYER_PUNT_RETURN_YARDS_COLUMN: Literal["punt_return_yards"] = "punt_return_yards"
PLAYER_SPECIAL_TEAM_FUMBLE_RETURNS_COLUMN: Literal["special_team_fumble_returns"] = (
    "special_team_fumble_returns"
)
PLAYER_SPECIAL_TEAM_FUMBLE_RETURN_YARDS_COLUMN: Literal[
    "special_team_fumble_return_yards"
] = "special_team_fumble_return_yards"
PLAYER_YARDS_PER_KICK_RETURN_COLUMN: Literal["yards_per_kick_return"] = (
    "yards_per_kick_return"
)
PLAYER_YARDS_PER_PUNT_RETURN_COLUMN: Literal["yards_per_punt_return"] = (
    "yards_per_punt_return"
)
PLAYER_YARDS_PER_RETURN_COLUMN: Literal["yards_per_return"] = "yards_per_return"
PLAYER_AVERAGE_PUNT_RETURN_YARDS_COLUMN: Literal["average_punt_return_yards"] = (
    "average_punt_return_yards"
)
PLAYER_GROSS_AVERAGE_PUNT_YARDS_COLUMN: Literal["gross_average_punt_yards"] = (
    "gross_average_punt_yards"
)
PLAYER_LONG_PUNT_COLUMN: Literal["long_punt"] = "long_punt"
PLAYER_NET_AVERAGE_PUNT_YARDS_COLUMN: Literal["net_average_punt_yards"] = (
    "net_average_punt_yards"
)
PLAYER_PUNTS_COLUMN: Literal["punts"] = "punts"
PLAYER_PUNTS_BLOCKED_COLUMN: Literal["punts_blocked"] = "punts_blocked"
PLAYER_PUNTS_BLOCKED_PERCENTAGE_COLUMN: Literal["punts_blocked_percentage"] = (
    "punts_blocked_percentage"
)
PLAYER_PUNTS_INSIDE_10_COLUMN: Literal["punts_inside_10"] = "punts_inside_10"
PLAYER_PUNTS_INSIDE_10_PERCENTAGE_COLUMN: Literal["punts_inside_10_percentage"] = (
    "punts_inside_10_percentage"
)
PLAYER_PUNTS_INSIDE_20_COLUMN: Literal["punts_inside_20"] = "punts_inside_20"
PLAYER_PUNTS_INSIDE_20_PERCENTAGE_COLUMN: Literal["punts_inside_20_percentage"] = (
    "punts_inside_20_percentage"
)
PLAYER_PUNTS_OVER_50_COLUMN: Literal["punts_over_50"] = "punts_over_50"
PLAYER_PUNT_YARDS_COLUMN: Literal["punt_yards"] = "punt_yards"
PLAYER_DEFENSIVE_POINTS_COLUMN: Literal["defensive_points"] = "defensive_points"
PLAYER_MISC_POINTS_COLUMN: Literal["misc_points"] = "misc_points"
PLAYER_RETURN_TOUCHDOWNS_COLUMN: Literal["return_touchdowns"] = "return_touchdowns"
PLAYER_TOTAL_TWO_POINT_CONVERSIONS_COLUMN: Literal["total_two_point_conversions"] = (
    "total_two_point_conversions"
)
PLAYER_PASSING_TOUCHDOWNS_9_YARDS_COLUMN: Literal["passing_touchdowns_9_yards"] = (
    "passing_touchdowns_9_yards"
)
PLAYER_PASSING_TOUCHDOWNS_19_YARDS_COLUMN: Literal["passing_touchdowns_19_yards"] = (
    "passing_touchdowns_19_yards"
)
PLAYER_PASSING_TOUCHDOWNS_29_YARDS_COLUMN: Literal["passing_touchdowns_29_yards"] = (
    "passing_touchdowns_29_yards"
)
PLAYER_PASSING_TOUCHDOWNS_39_YARDS_COLUMN: Literal["passing_touchdowns_39_yards"] = (
    "passing_touchdowns_39_yards"
)
PLAYER_PASSING_TOUCHDOWNS_49_YARDS_COLUMN: Literal["passing_touchdowns_49_yards"] = (
    "passing_touchdowns_49_yards"
)
PLAYER_PASSING_TOUCHDOWNS_ABOVE_50_YARDS_COLUMN: Literal[
    "passing_touchdowns_above_50_yards"
] = "passing_touchdowns_above_50_yards"
PLAYER_RECEIVING_TOUCHDOWNS_9_YARDS_COLUMN: Literal["receiving_touchdowns_9_yards"] = (
    "receiving_touchdowns_9_yards"
)
PLAYER_RECEIVING_TOUCHDOWNS_19_YARDS_COLUMN: Literal[
    "receiving_touchdowns_19_yards"
] = "receiving_touchdowns_19_yards"
PLAYER_RECEIVING_TOUCHDOWNS_29_YARDS_COLUMN: Literal[
    "receiving_touchdowns_29_yards"
] = "receiving_touchdowns_29_yards"
PLAYER_RECEIVING_TOUCHDOWNS_39_YARDS_COLUMN: Literal[
    "receiving_touchdowns_39_yards"
] = "receiving_touchdowns_39_yards"
PLAYER_RECEIVING_TOUCHDOWNS_49_YARDS_COLUMN: Literal[
    "receiving_touchdowns_49_yards"
] = "receiving_touchdowns_49_yards"
PLAYER_RECEIVING_TOUCHDOWNS_ABOVE_50_YARDS_COLUMN: Literal[
    "receiving_touchdowns_above_50_yards"
] = "receiving_touchdowns_above_50_yards"
PLAYER_RUSHING_TOUCHDOWNS_9_YARDS_COLUMN: Literal["rushing_touchdowns_9_yards"] = (
    "rushing_touchdowns_9_yards"
)
PLAYER_RUSHING_TOUCHDOWNS_19_YARDS_COLUMN: Literal["rushing_touchdowns_19_yards"] = (
    "rushing_touchdowns_19_yards"
)
PLAYER_RUSHING_TOUCHDOWNS_29_YARDS_COLUMN: Literal["rushing_touchdowns_29_yards"] = (
    "rushing_touchdowns_29_yards"
)
PLAYER_RUSHING_TOUCHDOWNS_39_YARDS_COLUMN: Literal["rushing_touchdowns_39_yards"] = (
    "rushing_touchdowns_39_yards"
)
PLAYER_RUSHING_TOUCHDOWNS_49_YARDS_COLUMN: Literal["rushing_touchdowns_49_yards"] = (
    "rushing_touchdowns_49_yards"
)
PLAYER_RUSHING_TOUCHDOWNS_ABOVE_50_YARDS_COLUMN: Literal[
    "rushing_touchdowns_above_50_yards"
] = "rushing_touchdowns_above_50_yards"
PLAYER_PENALTIES_IN_MINUTES_COLUMN: Literal["penalties_in_minutes"] = (
    "penalties_in_minutes"
)
PLAYER_EVEN_STRENGTH_GOALS_COLUMN: Literal["even_strength_goals"] = (
    "even_strength_goals"
)
PLAYER_POWER_PLAY_GOALS_COLUMN: Literal["power_play_goals"] = "power_play_goals"
PLAYER_SHORT_HANDED_GOALS_COLUMN: Literal["short_handed_goals"] = "short_handed_goals"
PLAYER_GAME_WINNING_GOALS_COLUMN: Literal["game_winning_goals"] = "game_winning_goals"
PLAYER_EVEN_STRENGTH_ASSISTS_COLUMN: Literal["even_strength_assists"] = (
    "even_strength_assists"
)
PLAYER_POWER_PLAY_ASSISTS_COLUMN: Literal["power_play_assists"] = "power_play_assists"
PLAYER_SHORT_HANDED_ASSISTS_COLUMN: Literal["short_handed_assists"] = (
    "short_handed_assists"
)
PLAYER_SHOTS_ON_GOAL_COLUMN: Literal["shots_on_goal"] = "shots_on_goal"
PLAYER_SHOOTING_PERCENTAGE_COLUMN: Literal["shooting_percentage"] = (
    "shooting_percentage"
)
PLAYER_SHIFTS_COLUMN: Literal["shifts"] = "shifts"
PLAYER_TIME_ON_ICE_COLUMN: Literal["time_on_ice"] = "time_on_ice"
PLAYER_DECISION_COLUMN: Literal["decision"] = "decision"
PLAYER_GOALS_AGAINST_COLUMN: Literal["goals_against"] = "goals_against"
PLAYER_SHOTS_AGAINST_COLUMN: Literal["shots_against"] = "shots_against"
PLAYER_SAVES_COLUMN: Literal["saves"] = "saves"
PLAYER_SAVE_PERCENTAGE_COLUMN: Literal["save_percentage"] = "save_percentage"
PLAYER_SHUTOUTS_COLUMN: Literal["shutouts"] = "shutouts"
PLAYER_INDIVIDUAL_CORSI_FOR_EVENTS_COLUMN: Literal["individual_corsi_for_events"] = (
    "individual_corsi_for_events"
)
PLAYER_ON_SHOT_ICE_FOR_EVENTS_COLUMN: Literal["on_shot_ice_for_events"] = (
    "on_shot_ice_for_events"
)
PLAYER_ON_SHOT_ICE_AGAINST_EVENTS_COLUMN: Literal["on_shot_ice_against_events"] = (
    "on_shot_ice_against_events"
)
PLAYER_CORSI_FOR_PERCENTAGE_COLUMN: Literal["corsi_for_percentage"] = (
    "corsi_for_percentage"
)
PLAYER_RELATIVE_CORSI_FOR_PERCENTAGE_COLUMN: Literal[
    "relative_corsi_for_percentage"
] = "relative_corsi_for_percentage"
PLAYER_OFFENSIVE_ZONE_STARTS_COLUMN: Literal["offensive_zone_starts"] = (
    "offensive_zone_starts"
)
PLAYER_DEFENSIVE_ZONE_STARTS_COLUMN: Literal["defensive_zone_starts"] = (
    "defensive_zone_starts"
)
PLAYER_OFFENSIVE_ZONE_START_PERCENTAGE_COLUMN: Literal[
    "offensive_zone_start_percentage"
] = "offensive_zone_start_percentage"
PLAYER_HITS_COLUMN: Literal["hits"] = "hits"
PLAYER_TRUE_SHOOTING_PERCENTAGE_COLUMN: Literal["true_shooting_percentage"] = (
    "true_shooting_percentage"
)
PLAYER_AT_BATS_COLUMN: Literal["at_bats"] = "at_bats"
PLAYER_RUNS_SCORED_COLUMN: Literal["runs_scored"] = "runs_scored"
PLAYER_RUNS_BATTED_IN_COLUMN: Literal["runs_batted_in"] = "runs_batted_in"
PLAYER_BASES_ON_BALLS_COLUMN: Literal["bases_on_balls"] = "bases_on_balls"
PLAYER_STRIKEOUTS_COLUMN: Literal["strikeouts"] = "strikeouts"
PLAYER_PLATE_APPEARANCES_COLUMN: Literal["plate_appearances"] = "plate_appearances"
PLAYER_HITS_AT_BATS_COLUMN: Literal["hits_at_bats"] = "hits_at_bats"
PLAYER_OBP_COLUMN: Literal["obp"] = "obp"
PLAYER_SLG_COLUMN: Literal["slg"] = "slg"
PLAYER_OPS_COLUMN: Literal["ops"] = "ops"
PLAYER_PITCHES_COLUMN: Literal["pitches"] = "pitches"
PLAYER_STRIKES_COLUMN: Literal["strikes"] = "strikes"
PLAYER_WIN_PROBABILITY_ADDED_COLUMN: Literal["win_probability_added"] = (
    "win_probability_added"
)
PLAYER_AVERAGE_LEVERAGE_INDEX_COLUMN: Literal["average_leverage_index"] = (
    "average_leverage_index"
)
PLAYER_WPA_PLUS_COLUMN: Literal["wpa_plus"] = "wpa_plus"
PLAYER_WPA_MINUS_COLUMN: Literal["wpa_minus"] = "wpa_minus"
PLAYER_CWPA_COLUMN: Literal["cwpa"] = "cwpa"
PLAYER_ACLI_COLUMN: Literal["acli"] = "acli"
PLAYER_RE24_COLUMN: Literal["re24"] = "re24"
PLAYER_PUTOUTS_COLUMN: Literal["putouts"] = "putouts"
PLAYER_INNINGS_PITCHED_COLUMN: Literal["innings_pitched"] = "innings_pitched"
PLAYER_EARNED_RUNS_COLUMN: Literal["earned_runs"] = "earned_runs"
PLAYER_HOME_RUNS_COLUMN: Literal["home_runs"] = "home_runs"
PLAYER_ERA_COLUMN: Literal["era"] = "era"
PLAYER_BATTERS_FACED_COLUMN: Literal["batters_faced"] = "batters_faced"
PLAYER_STRIKES_BY_CONTACT_COLUMN: Literal["strikes_by_contact"] = "strikes_by_contact"
PLAYER_STRIKES_SWINGING_COLUMN: Literal["strikes_swinging"] = "strikes_swinging"
PLAYER_STRIKES_LOOKING_COLUMN: Literal["strikes_looking"] = "strikes_looking"
PLAYER_GROUND_BALLS_COLUMN: Literal["ground_balls"] = "ground_balls"
PLAYER_FLY_BALLS_COLUMN: Literal["fly_balls"] = "fly_balls"
PLAYER_LINE_DRIVES_COLUMN: Literal["line_drives"] = "line_drives"
PLAYER_INHERITED_RUNNERS_COLUMN: Literal["inherited_runners"] = "inherited_runners"
PLAYER_INHERITED_SCORES_COLUMN: Literal["inherited_scores"] = "inherited_scores"
PLAYER_EFFECTIVE_FIELD_GOAL_PERCENTAGE_COLUMN: Literal[
    "effective_field_goal_percentage"
] = "effective_field_goal_percentage"
PLAYER_PENALTY_KICKS_MADE_COLUMN: Literal["penalty_kicks_made"] = "penalty_kicks_made"
PLAYER_PENALTY_KICKS_ATTEMPTED_COLUMN: Literal["penalty_kicks_attempted"] = (
    "penalty_kicks_attempted"
)
PLAYER_SHOTS_TOTAL_COLUMN: Literal["shots_total"] = "shots_total"
PLAYER_SHOTS_ON_TARGET_COLUMN: Literal["shots_on_target"] = "shots_on_target"
PLAYER_YELLOW_CARDS_COLUMN: Literal["yellow_cards"] = "yellow_cards"
PLAYER_RED_CARDS_COLUMN: Literal["red_cards"] = "red_cards"
PLAYER_TOUCHES_COLUMN: Literal["touches"] = "touches"
PLAYER_EXPECTED_GOALS_COLUMN: Literal["expected_goals"] = "expected_goals"
PLAYER_NON_PENALTY_EXPECTED_GOALS_COLUMN: Literal["non_penalty_expected_goals"] = (
    "non_penalty_expected_goals"
)
PLAYER_EXPECTED_ASSISTED_GOALS_COLUMN: Literal["expected_assisted_goals"] = (
    "expected_assisted_goals"
)
PLAYER_SHOT_CREATING_ACTIONS_COLUMN: Literal["shot_creating_actions"] = (
    "shot_creating_actions"
)
PLAYER_GOAL_CREATING_ACTIONS_COLUMN: Literal["goal_creating_actions"] = (
    "goal_creating_actions"
)
PLAYER_PASSES_COMPLETED_COLUMN: Literal["passes_completed"] = "passes_completed"
PLAYER_PASSES_ATTEMPTED_COLUMN: Literal["passes_attempted"] = "passes_attempted"
PLAYER_PASS_COMPLETION_COLUMN: Literal["pass_completion"] = "pass_completion"
PLAYER_PROGRESSIVE_PASSES_COLUMN: Literal["progressive_passes"] = "progressive_passes"
PLAYER_CARRIES_COLUMN: Literal["carries"] = "carries"
PLAYER_PROGRESSIVE_CARRIES_COLUMN: Literal["progressive_carries"] = (
    "progressive_carries"
)
PLAYER_TAKE_ONS_ATTEMPTED_COLUMN: Literal["take_ons_attempted"] = "take_ons_attempted"
PLAYER_SUCCESSFUL_TAKE_ONS_COLUMN: Literal["successful_take_ons"] = (
    "successful_take_ons"
)
PLAYER_TOTAL_PASSING_DISTANCE_COLUMN: Literal["total_passing_distance"] = (
    "total_passing_distance"
)
PLAYER_PROGRESSIVE_PASSING_DISTANCE_COLUMN: Literal["progressive_passing_distance"] = (
    "progressive_passing_distance"
)
PLAYER_PASSES_COMPLETED_SHORT_COLUMN: Literal["passes_completed_short"] = (
    "passes_completed_short"
)
PLAYER_PASSES_ATTEMPTED_SHORT_COLUMN: Literal["passes_attempted_short"] = (
    "passes_attempted_short"
)
PLAYER_PASS_COMPLETION_SHORT_COLUMN: Literal["pass_completion_short"] = (
    "pass_completion_short"
)
PLAYER_PASSES_COMPLETED_MEDIUM_COLUMN: Literal["passes_completed_medium"] = (
    "passes_completed_medium"
)
PLAYER_PASSES_ATTEMPTED_MEDIUM_COLUMN: Literal["passes_attempted_medium"] = (
    "passes_attempted_medium"
)
PLAYER_PASS_COMPLETION_MEDIUM_COLUMN: Literal["pass_completion_medium"] = (
    "pass_completion_medium"
)
PLAYER_PASSES_COMPLETED_LONG_COLUMN: Literal["passes_completed_long"] = (
    "passes_completed_long"
)
PLAYER_PASSES_ATTEMPTED_LONG_COLUMN: Literal["passes_attempted_long"] = (
    "passes_attempted_long"
)
PLAYER_PASS_COMPLETION_LONG_COLUMN: Literal["pass_completion_long"] = (
    "pass_completion_long"
)
PLAYER_EXPECTED_ASSISTS_COLUMN: Literal["expected_assists"] = "expected_assists"
PLAYER_KEY_PASSES_COLUMN: Literal["key_passes"] = "key_passes"
PLAYER_PASSES_INTO_FINAL_THIRD_COLUMN: Literal["passes_into_final_third"] = (
    "passes_into_final_third"
)
PLAYER_PASSES_INTO_PENALTY_AREA_COLUMN: Literal["passes_into_penalty_area"] = (
    "passes_into_penalty_area"
)
PLAYER_CROSSES_INTO_PENALTY_AREA_COLUMN: Literal["crosses_into_penalty_area"] = (
    "crosses_into_penalty_area"
)
PLAYER_LIVE_BALL_PASSES_COLUMN: Literal["live_ball_passes"] = "live_ball_passes"
PLAYER_DEAD_BALL_PASSES_COLUMN: Literal["dead_ball_passes"] = "dead_ball_passes"
PLAYER_PASSES_FROM_FREE_KICKS_COLUMN: Literal["passes_from_free_kicks"] = (
    "passes_from_free_kicks"
)
PLAYER_THROUGH_BALLS_COLUMN: Literal["through_balls"] = "through_balls"
PLAYER_SWITCHES_COLUNM: Literal["switches"] = "switches"
PLAYER_CROSSES_COLUMN: Literal["crosses"] = "crosses"
PLAYER_THROW_INS_TAKEN_COLUMN: Literal["throw_ins_taken"] = "throw_ins_taken"
PLAYER_CORNER_KICKS_COLUMN: Literal["corner_kicks"] = "corner_kicks"
PLAYER_INSWINGING_CORNER_KICKS_COLUMN: Literal["inswinging_corner_kicks"] = (
    "inswinging_corner_kicks"
)
PLAYER_OUTSWINGING_CORNER_KICKS_COLUMN: Literal["outswinging_corner_kicks"] = (
    "outswinging_corner_kicks"
)
PLAYER_STRAIGHT_CORNER_KICKS_COLUMN: Literal["straight_corner_kicks"] = (
    "straight_corner_kicks"
)
PLAYER_PASSES_OFFSIDE_COLUMN: Literal["passes_offside"] = "passes_offside"
PLAYER_PASSES_BLOCKED_COLUMN: Literal["passes_blocked"] = "passes_blocked"
PLAYER_TACKLES_WON_COLUMN: Literal["tackles_won"] = "tackles_won"
PLAYER_TACKLES_IN_DEFENSIVE_THIRD_COLUMN: Literal["tackles_in_defensive_third"] = (
    "tackles_in_defensive_third"
)
PLAYER_TACKLES_IN_MIDDLE_THIRD_COLUMN: Literal["tackles_in_middle_third"] = (
    "tackles_in_middle_third"
)
PLAYER_TACKLES_IN_ATTACKING_THIRD_COLUMN: Literal["tackles_in_attacking_third"] = (
    "tackles_in_attacking_third"
)
PLAYER_DRIBBLERS_TACKLED_COLUMN: Literal["dribblers_tackled"] = "dribblers_tackled"
PLAYER_DRIBBLES_CHALLENGED_COLUMN: Literal["dribbles_challenged"] = (
    "dribbles_challenged"
)
PLAYER_PERCENT_OF_DRIBBLERS_TACKLED_COLUMN: Literal["percent_of_dribblers_tackled"] = (
    "percent_of_dribblers_tackled"
)
PLAYER_CHALLENGES_LOST_COLUMN: Literal["challenges_lost"] = "challenges_lost"
PLAYER_SHOTS_BLOCKED_COLUMN: Literal["shots_blocked"] = "shots_blocked"
PLAYER_TACKLES_PLUS_INTERCEPTIONS_COLUMN: Literal["tackles_plus_interceptions"] = (
    "tackles_plus_interceptions"
)
PLAYER_ERRORS_COLUMN: Literal["errors"] = "errors"
PLAYER_TOUCHES_IN_DEFENSIVE_PENALTY_AREA_COLUMN: Literal[
    "touches_in_defensive_penalty_area"
] = "touches_in_defensive_penalty_area"
PLAYER_TOUCHES_IN_DEFENSIVE_THIRD_COLUMN: Literal["touches_in_defensive_third"] = (
    "touches_in_defensive_third"
)
PLAYER_TOUCHES_IN_MIDDLE_THIRD_COLUMN: Literal["touches_in_middle_third"] = (
    "touches_in_middle_third"
)
PLAYER_TOUCHES_IN_ATTACKING_THIRD_COLUMN: Literal["touches_in_attacking_third"] = (
    "touches_in_attacking_third"
)
PLAYER_TOUCHES_IN_ATTACKING_PENALTY_AREA_COLUMN: Literal[
    "touches_in_attacking_penalty_area"
] = "touches_in_attacking_penalty_area"
PLAYER_LIVE_BALL_TOUCHES_COLUMN: Literal["live_ball_touches"] = "live_ball_touches"
PLAYER_SUCCESSFUL_TAKE_ON_PERCENTAGE_COLUMN: Literal[
    "successful_take_on_percentage"
] = "successful_take_on_percentage"
PLAYER_TIMES_TACKLED_DURING_TAKE_ONS_COLUMN: Literal[
    "times_tackled_during_take_ons"
] = "times_tackled_during_take_ons"
PLAYER_TACKLED_DURING_TAKE_ON_PERCENTAGE_COLUMN: Literal[
    "tackled_during_take_on_percentage"
] = "tackled_during_take_on_percentage"
PLAYER_TOTAL_CARRYING_DISTANCE_COLUMN: Literal["total_carrying_distance"] = (
    "total_carrying_distance"
)
PLAYER_PROGRESSIVE_CARRYING_DISTANCE_COLUMN: Literal[
    "progressive_carrying_distance"
] = "progressive_carrying_distance"
PLAYER_CARRIES_INTO_FINAL_THIRD_COLUMN: Literal["carries_into_final_third"] = (
    "carries_into_final_third"
)
PLAYER_CARRIES_INTO_PENALTY_AREA_COLUMN: Literal["carries_into_penalty_area"] = (
    "carries_into_penalty_area"
)
PLAYER_MISCONTROLS_COLUMN: Literal["miscontrols"] = "miscontrols"
PLAYER_DISPOSSESSED_COLUMN: Literal["dispossessed"] = "dispossessed"
PLAYER_PASSES_RECEIVED_COLUMN: Literal["passes_received"] = "passes_received"
PLAYER_PROGRESSIVE_PASSES_RECEIVED_COLUMN: Literal["progressive_passes_received"] = (
    "progressive_passes_received"
)
PLAYER_SECOND_YELLOW_CARD_COLUMN: Literal["second_yellow_card"] = "second_yellow_card"
PLAYER_FOULS_COMMITTED_COLUMN: Literal["fouls_committed"] = "fouls_committed"
PLAYER_FOULS_DRAWN_COLUMN: Literal["fouls_drawn"] = "fouls_drawn"
PLAYER_OFFSIDES_COLUMN: Literal["offsides"] = "offsides"
PLAYER_PENALTY_KICKS_WON_COLUMN: Literal["penalty_kicks_won"] = "penalty_kicks_won"
PLAYER_PENALTY_KICKS_CONCEDED_COLUMN: Literal["penalty_kicks_conceded"] = (
    "penalty_kicks_conceded"
)
PLAYER_OWN_GOALS_COLUMN: Literal["own_goals"] = "own_goals"
PLAYER_BALL_RECOVERIES_COLUMN: Literal["ball_recoveries"] = "ball_recoveries"
PLAYER_AERIALS_WON_COLUMN: Literal["aerials_won"] = "aerials_won"
PLAYER_AERIALS_LOST_COLUMN: Literal["aerials_lost"] = "aerials_lost"
PLAYER_PERCENTAGE_OF_AERIALS_WON_COLUMN: Literal["percentage_of_aerials_won"] = (
    "percentage_of_aerials_won"
)
PLAYER_SHOTS_ON_TARGET_AGAINST_COLUMN: Literal["shots_on_target_against"] = (
    "shots_on_target_against"
)
PLAYER_POST_SHOT_EXPECTED_GOALS_COLUMN: Literal["post_shot_expected_goals"] = (
    "post_shot_expected_goals"
)
PLAYER_PASSES_ATTEMPTED_MINUS_GOAL_KICKS_COLUMN: Literal[
    "passes_attempted_minus_goal_kicks"
] = "passes_attempted_minus_goal_kicks"
PLAYER_THROWS_ATTEMPTED_COLUMN: Literal["throws_attempted"] = "throws_attempted"
PLAYER_PERCENTAGE_OF_PASSES_THAT_WERE_LAUNCHED_COLUMN: Literal[
    "percentage_of_passes_that_were_launched"
] = "percentage_of_passes_that_were_launched"
PLAYER_AVERAGE_PASS_LENGTH_COLUMN: Literal["average_pass_length"] = (
    "average_pass_length"
)
PLAYER_GOAL_KICKS_ATTEMPTED_COLUMN: Literal["goal_kicks_attempted"] = (
    "goal_kicks_attempted"
)
PLAYER_PERCENTAGE_OF_GOAL_KICKS_THAT_WERE_LAUNCHED_COLUMN: Literal[
    "percentage_of_goal_kicks_that_were_launched"
] = "percentage_of_goal_kicks_that_were_launched"
PLAYER_AVERAGE_GOAL_KICK_LENGTH_COLUMN: Literal["average_goal_kick_length"] = (
    "average_goal_kick_length"
)
PLAYER_CROSSES_FACED_COLUMN: Literal["crosses_faced"] = "crosses_faced"
PLAYER_CROSSES_STOPPED_COLUMN: Literal["crosses_stopped"] = "crosses_stopped"
PLAYER_PERCENTAGE_CROSSES_STOPPED_COLUMN: Literal["percentage_crosses_stopped"] = (
    "percentage_crosses_stopped"
)
PLAYER_DEFENSIVE_ACTIONS_OUTSIDE_PENALTY_AREA_COLUMN: Literal[
    "defensive_actions_outside_penalty_area"
] = "defensive_actions_outside_penalty_area"
PLAYER_AVERAGE_DISTANCE_OF_DEFENSIVE_ACTIONS_COLUMN: Literal[
    "average_distance_of_defensive_actions"
] = "average_distance_of_defensive_actions"
PLAYER_THREE_POINT_ATTEMPT_RATE_COLUMN: Literal["three_point_attempt_rate"] = (
    "three_point_attempt_rate"
)
VERSION = DELIMITER.join(["0.0.5", ADDRESS_VERSION, OWNER_VERSION, VENUE_VERSION])


def _guess_sex(data: dict[str, Any]) -> str | None:
    name = data[PLAYER_NAME_COLUMN]
    gender_tag = GENDER_DETECTOR.get_gender(name)
    if gender_tag in MALE_GENDERS:
        return str(Sex.MALE)
    if gender_tag in FEMALE_GENDERS:
        return str(Sex.FEMALE)
    if gender_tag in UNCERTAIN_GENDERS:
        return None
    return None


def _calculate_field_goals_percentage(data: dict[str, Any]) -> float | None:
    field_goals = data.get(FIELD_GOALS_COLUMN)
    if field_goals is None:
        return None
    field_goals_attempted = data.get(FIELD_GOALS_ATTEMPTED_COLUMN)
    if field_goals_attempted is None:
        return None
    if field_goals_attempted == 0:
        return 0.0
    return float(field_goals) / float(field_goals_attempted)  # type: ignore


def _calculate_three_point_field_goals_percentage(data: dict[str, Any]) -> float | None:
    three_point_field_goals = data.get(PLAYER_THREE_POINT_FIELD_GOALS_COLUMN)
    if three_point_field_goals is None:
        return None
    three_point_field_goals_attempted = data.get(
        PLAYER_THREE_POINT_FIELD_GOALS_ATTEMPTED_COLUMN
    )
    if three_point_field_goals_attempted is None:
        return None
    if three_point_field_goals_attempted == 0:
        return 0.0
    return float(three_point_field_goals) / float(three_point_field_goals_attempted)  # type: ignore


def _calculate_free_throws_percentage(data: dict[str, Any]) -> float | None:
    free_throws = data.get(PLAYER_FREE_THROWS_COLUMN)
    if free_throws is None:
        return None
    free_throws_attempted = data.get(PLAYER_FREE_THROWS_ATTEMPTED_COLUMN)
    if free_throws_attempted is None:
        return None
    if free_throws_attempted == 0:
        return 0.0
    return float(free_throws) / float(free_throws_attempted)  # type: ignore


def _calculate_total_rebounds(data: dict[str, Any]) -> int | None:
    offensive_rebounds = data.get(OFFENSIVE_REBOUNDS_COLUMN)
    if offensive_rebounds is None:
        return None
    defensive_rebounds = data.get(PLAYER_DEFENSIVE_REBOUNDS_COLUMN)
    if defensive_rebounds:
        return None
    return offensive_rebounds + defensive_rebounds


class PlayerModel(BaseModel):
    """The serialisable player class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=PLAYER_IDENTIFIER_COLUMN,
    )
    jersey: str | None = Field(None, json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKS_COLUMN,
    )
    fumbles: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_COLUMN,
    )
    fumbles_lost: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_LOST_COLUMN,
    )
    field_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_COLUMN,
    )
    field_goals_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=FIELD_GOALS_ATTEMPTED_COLUMN,
    )
    offensive_rebounds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=OFFENSIVE_REBOUNDS_COLUMN,
    )
    assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ASSISTS_COLUMN,
    )
    turnovers: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=TURNOVERS_COLUMN,
    )
    name: str = Field(..., alias=PLAYER_NAME_COLUMN)
    marks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MARKS_COLUMN,
    )
    handballs: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_HANDBALLS_COLUMN,
    )
    disposals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DISPOSALS_COLUMN,
    )
    goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GOALS_COLUMN,
    )
    behinds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BEHINDS_COLUMN,
    )
    hit_outs: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_HIT_OUTS_COLUMN,
    )
    tackles: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_COLUMN,
    )
    rebounds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_REBOUNDS_COLUMN,
    )
    insides: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INSIDES_COLUMN,
    )
    clearances: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CLEARANCES_COLUMN,
    )
    clangers: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CLANGERS_COLUMN,
    )
    free_kicks_for: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FREE_KICKS_FOR_COLUMN,
    )
    free_kicks_against: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FREE_KICKS_AGAINST_COLUMN,
    )
    brownlow_votes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BROWNLOW_VOTES_COLUMN,
    )
    contested_possessions: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CONTESTED_POSSESSIONS_COLUMN,
    )
    uncontested_possessions: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_UNCONTESTED_POSSESSIONS_COLUMN,
    )
    contested_marks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CONTESTED_MARKS_COLUMN,
    )
    marks_inside: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MARKS_INSIDE_COLUMN,
    )
    one_percenters: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ONE_PERCENTERS_COLUMN,
    )
    bounces: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BOUNCES_COLUMN,
    )
    goal_assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GOAL_ASSISTS_COLUMN,
    )
    percentage_played: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERCENTAGE_PLAYED_COLUMN,
    )
    birth_date: datetime.date | None = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_BIRTH_DATE_COLUMN
    )
    species: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL, FFILL_KEY: True},
        alias=PLAYER_SPECIES_COLUMN,
    )
    handicap_weight: float | None = Field(None, alias=PLAYER_HANDICAP_WEIGHT_COLUMN)
    father: PlayerModel | None = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_FATHER_COLUMN
    )
    sex: str | None = Field(
        default_factory=_guess_sex,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL, FFILL_KEY: True},
        alias=PLAYER_SEX_COLUMN,
    )
    age: int | None = Field(None, alias=PLAYER_AGE_COLUMN)
    starting_position: str | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=PLAYER_STARTING_POSITION_COLUMN,
    )
    weight: float | None = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_WEIGHT_COLUMN
    )
    birth_address: AddressModel | None = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_BIRTH_ADDRESS_COLUMN
    )
    owner: OwnerModel | None = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_OWNER_COLUMN
    )
    seconds_played: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SECONDS_PLAYED_COLUMN,
    )
    field_goals_percentage: float | None = Field(
        default_factory=_calculate_field_goals_percentage,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_PERCENTAGE_COLUMN,
    )
    three_point_field_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_THREE_POINT_FIELD_GOALS_COLUMN,
    )
    three_point_field_goals_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_THREE_POINT_FIELD_GOALS_ATTEMPTED_COLUMN,
    )
    three_point_field_goals_percentage: float | None = Field(
        default_factory=_calculate_three_point_field_goals_percentage,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_THREE_POINT_FIELD_GOALS_PERCENTAGE_COLUMN,
    )
    free_throws: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FREE_THROWS_COLUMN,
    )
    free_throws_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FREE_THROWS_ATTEMPTED_COLUMN,
    )
    free_throws_percentage: float | None = Field(
        default_factory=_calculate_free_throws_percentage,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FREE_THROWS_PERCENTAGE_COLUMN,
    )
    defensive_rebounds: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_REBOUNDS_COLUMN,
    )
    total_rebounds: int | None = Field(
        default_factory=_calculate_total_rebounds,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_REBOUNDS_COLUMN,
    )
    steals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STEALS_COLUMN,
    )
    blocks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BLOCKS_COLUMN,
    )
    personal_fouls: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERSONAL_FOULS_COLUMN,
    )
    points: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_POINTS_COLUMN,
    )
    game_score: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GAME_SCORE_COLUMN,
    )
    point_differential: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_POINT_DIFFERENTIAL_COLUMN,
    )
    version: str
    height: float | None = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_HEIGHT_COLUMN
    )
    colleges: list[VenueModel] = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_COLLEGES_COLUMN
    )
    headshot: str | None = Field(
        ..., json_schema_extra={FFILL_KEY: True}, alias=PLAYER_HEADSHOT_COLUMN
    )
    forced_fumbles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FORCED_FUMBLES_COLUMN,
    )
    fumbles_recovered: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_RECOVERED_COLUMN,
    )
    fumbles_recovered_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_RECOVERED_YARDS_COLUMN,
    )
    fumbles_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLES_TOUCHDOWNS_COLUMN,
    )
    offensive_two_point_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OFFENSIVE_TWO_POINT_RETURNS_COLUMN,
    )
    offensive_fumbles_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OFFENSIVE_FUMBLES_TOUCHDOWNS_COLUMN,
    )
    defensive_fumbles_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_FUMBLES_TOUCHDOWNS_COLUMN,
    )
    average_gain: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_GAIN_COLUMN,
    )
    completion_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_COMPLETION_PERCENTAGE_COLUMN,
    )
    completions: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_COMPLETIONS_COLUMN,
    )
    espn_quarterback_rating: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ESPN_QUARTERBACK_RATING_COLUMN,
    )
    interception_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INTERCEPTION_PERCENTAGE_COLUMN,
    )
    interceptions: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INTERCEPTIONS_COLUMN,
    )
    long_passing: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_PASSING_COLUMN,
    )
    misc_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MISC_YARDS_COLUMN,
    )
    net_passing_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_NET_PASSING_YARDS_COLUMN,
    )
    net_total_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_NET_TOTAL_YARDS_COLUMN,
    )
    passing_attempts: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_ATTEMPTS_COLUMN,
    )
    passing_big_plays: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_BIG_PLAYS_COLUMN,
    )
    passing_first_downs: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_FIRST_DOWNS_COLUMN,
    )
    passing_fumbles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_FUMBLES_COLUMN,
    )
    passing_fumbles_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_FUMBLES_LOST_COLUMN,
    )
    passing_touchdown_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWN_PERCENTAGE_COLUMN,
    )
    passing_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWNS_COLUMN,
    )
    passing_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_YARDS_COLUMN,
    )
    passing_yards_after_catch: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_YARDS_AFTER_CATCH_COLUMN,
    )
    passing_yards_at_catch: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_YARDS_AT_CATCH_COLUMN,
    )
    quarterback_rating: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_QUARTERBACK_RATING_COLUMN,
    )
    sacks: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SACKS_COLUMN,
    )
    sacks_yards_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SACKS_YARDS_LOST_COLUMN,
    )
    net_passing_attempts: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_NET_PASSING_ATTEMPTS_COLUMN,
    )
    total_offensive_plays: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_OFFENSIVE_PLAYS_COLUMN,
    )
    total_points: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_POINTS_COLUMN,
    )
    total_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_TOUCHDOWNS_COLUMN,
    )
    total_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_YARDS_COLUMN,
    )
    total_yards_from_scrimmage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_YARDS_FROM_SCRIMMAGE_COLUMN,
    )
    two_point_pass: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TWO_POINT_PASS_COLUMN,
    )
    two_point_pass_attempt: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TWO_POINT_PASS_ATTEMPT_COLUMN,
    )
    yards_per_completion: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_PER_COMPLETION_COLUMN,
    )
    yards_per_pass_attempt: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_PER_PASS_ATTEMPT_COLUMN,
    )
    net_yards_per_pass_attempt: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_NET_YARDS_PER_PASS_ATTEMPT_COLUMN,
    )
    long_rushing: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_RUSHING_COLUMN,
    )
    rushing_attempts: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_ATTEMPTS_COLUMN,
    )
    rushing_big_plays: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_BIG_PLAYS_COLUMN,
    )
    rushing_first_downs: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_FIRST_DOWNS_COLUMN,
    )
    rushing_fumbles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_FUMBLES_COLUMN,
    )
    rushing_fumbles_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_FUMBLES_LOST_COLUMN,
    )
    rushing_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_TOUCHDOWNS_COLUMN,
    )
    rushing_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_YARDS_COLUMN,
    )
    stuffs: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STUFFS_COLUMN,
    )
    stuff_yards_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STUFF_YARDS_LOST,
    )
    two_point_rush: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TWO_POINT_RUSH_COLUMN,
    )
    two_point_rush_attempts: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TWO_POINT_RUSH_ATTEMPTS_COLUMN,
    )
    yards_per_rush_attempt: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_PER_RUSH_ATTEMPT_COLUMN,
    )
    espn_widereceiver: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ESPN_WIDERECEIVER_COLUMN,
    )
    long_reception: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_RECEPTION_COLUMN,
    )
    receiving_big_plays: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_BIG_PLAYS_COLUMN,
    )
    receiving_first_downs: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_FIRST_DOWNS_COLUMN,
    )
    receiving_fumbles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_FUMBLES_COLUMN,
    )
    receiving_fumbles_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_FUMBLES_LOST_COLUMN,
    )
    receiving_targets: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TARGETS_COLUMN,
    )
    receiving_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TOUCHDOWNS_COLUMN,
    )
    receiving_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_YARDS_COLUMN,
    )
    receiving_yards_after_catch: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_YARDS_AFTER_CATCH_COLUMN,
    )
    receiving_yards_at_catch: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_YARDS_AT_CATCH_COLUMN,
    )
    receptions: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEPTIONS_COLUMN,
    )
    two_point_receptions: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TWO_POINT_RECEPTIONS_COLUMN,
    )
    two_point_reception_attempts: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TWO_POINT_RECEPTION_ATTEMPTS_COLUMN,
    )
    yards_per_reception: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_PER_RECEPTION_COLUMN,
    )
    assist_tackles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ASSIST_TACKLES_COLUMN,
    )
    average_interception_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_INTERCEPTION_YARDS_COLUMN,
    )
    average_sack_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_SACK_YARDS_COLUMN,
    )
    average_stuff_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_STUFF_YARDS_COLUMN,
    )
    blocked_field_goal_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BLOCKED_FIELD_GOAL_TOUCHDOWNS_COLUMN,
    )
    blocked_punt_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BLOCKED_PUNT_TOUCHDOWNS_COLUMN,
    )
    defensive_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_TOUCHDOWNS_COLUMN,
    )
    hurries: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_HURRIES_COLUMN,
    )
    kicks_blocked: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKS_BLOCKED_COLUMN,
    )
    long_interception: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_INTERCEPTION_COLUMN,
    )
    misc_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MISC_TOUCHDOWNS_COLUMN,
    )
    passes_batted_down: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_BATTED_DOWN_COLUMN,
    )
    passes_defended: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_DEFENDED_COLUMN,
    )
    quarterback_hits: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_QUARTERBACK_HITS_COLUMN,
    )
    sacks_assisted: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SACKS_ASSISTED_COLUMN,
    )
    sacks_unassisted: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SACKS_UNASSISTED_COLUMN,
    )
    sacks_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SACKS_YARDS_COLUMN,
    )
    safeties: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SAFETIES_COLUMN,
    )
    solo_tackles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SOLO_TACKLES_COLUMN,
    )
    stuff_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STUFF_YARDS_COLUMN,
    )
    tackles_for_loss: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_FOR_LOSS_COLUMN,
    )
    tackles_yards_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_YARDS_LOST_COLUMN,
    )
    yards_allowed: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_ALLOWED_COLUMN,
    )
    points_allowed: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_POINTS_ALLOWED_COLUMN,
    )
    one_point_safeties_made: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ONE_POINT_SAFETIES_MADE_COLUMN,
    )
    missed_field_goal_return_td: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MISSED_FIELD_GOAL_RETURN_TD_COLUMN,
    )
    blocked_punt_ez_rec_td: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BLOCKED_PUNT_EZ_REC_TD_COLUMN,
    )
    interception_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INTERCEPTION_TOUCHDOWNS_COLUMN,
    )
    interception_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INTERCEPTION_YARDS_COLUMN,
    )
    average_kickoff_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_KICKOFF_RETURN_YARDS_COLUMN,
    )
    average_kickoff_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_KICKOFF_YARDS_COLUMN,
    )
    extra_point_attempts: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXTRA_POINT_ATTEMPTS_COLUMN,
    )
    extra_point_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXTRA_POINT_PERCENTAGE_COLUMN,
    )
    extra_point_blocked: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXTRA_POINT_BLOCKED_COLUMN,
    )
    extra_points_blocked_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXTRA_POINTS_BLOCKED_PERCENTAGE_COLUMN,
    )
    extra_points_made: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXTRA_POINTS_MADE_COLUMN,
    )
    fair_catches: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FAIR_CATCHES_COLUMN,
    )
    fair_catch_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FAIR_CATCH_PERCENTAGE_COLUMN,
    )
    field_goal_attempts_max_19_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPTS_MAX_19_YARDS_COLUMN,
    )
    field_goal_attempts_max_29_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPTS_MAX_29_YARDS_COLUMN,
    )
    field_goal_attempts_max_39_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPTS_MAX_39_YARDS_COLUMN,
    )
    field_goal_attempts_max_49_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPTS_MAX_49_YARDS_COLUMN,
    )
    field_goal_attempts_max_59_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPTS_MAX_59_YARDS_COLUMN,
    )
    field_goal_attempts_max_99_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPTS_MAX_99_YARDS_COLUMN,
    )
    field_goal_attempts_above_50_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPTS_ABOVE_50_YARDS_COLUMN,
    )
    field_goal_attempt_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOAL_ATTEMPT_YARDS_COLUMN,
    )
    field_goals_blocked: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_BLOCKED_COLUMN,
    )
    field_goals_blocked_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_BLOCKED_PERCENTAGE_COLUMN,
    )
    field_goals_made: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_COLUMN,
    )
    field_goals_made_max_19_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_MAX_19_YARDS_COLUMN,
    )
    field_goals_made_max_29_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_MAX_29_YARDS_COLUMN,
    )
    field_goals_made_max_39_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_MAX_39_YARDS_COLUMN,
    )
    field_goals_made_max_49_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_MAX_49_YARDS_COLUMN,
    )
    field_goals_made_max_59_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_MAX_59_YARDS_COLUMN,
    )
    field_goals_made_max_99_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_MAX_99_YARDS_COLUMN,
    )
    field_goals_made_above_50_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_ABOVE_50_YARDS_COLUMN,
    )
    field_goals_made_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MADE_YARDS_COLUMN,
    )
    field_goals_missed_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FIELD_GOALS_MISSED_YARDS_COLUMN,
    )
    kickoff_out_of_bounds: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKOFF_OUT_OF_BOUNDS_COLUMN,
    )
    kickoff_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKOFF_RETURNS_COLUMN,
    )
    kickoff_returns_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKOFF_RETURNS_TOUCHDOWNS_COLUMN,
    )
    kickoff_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKOFF_RETURN_YARDS_COLUMN,
    )
    kickoffs: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKOFFS_COLUMN,
    )
    kickoff_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICKOFF_YARDS_COLUMN,
    )
    long_field_goal_attempt: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_FIELD_GOAL_ATTEMPT_COLUMN,
    )
    long_field_goal_made: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_FIELD_GOAL_MADE_COLUMN,
    )
    long_kickoff: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_KICKOFF_COLUMN,
    )
    total_kicking_points: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_KICKING_POINTS_COLUMN,
    )
    touchback_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHBACK_PERCENTAGE_COLUMN,
    )
    touchbacks: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHBACKS_COLUMN,
    )
    defensive_fumble_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_FUMBLE_RETURNS_COLUMN,
    )
    defensive_fumble_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_FUMBLE_RETURN_YARDS_COLUMN,
    )
    fumble_recoveries: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLE_RECOVERIES_COLUMN,
    )
    fumble_recovery_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FUMBLE_RECOVERY_YARDS_COLUMN,
    )
    kick_return_fair_catches: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICK_RETURN_FAIR_CATCHES_COLUMN,
    )
    kick_return_fair_catch_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICK_RETURN_FAIR_CATCH_PERCENTAGE_COLUMN,
    )
    kick_return_fumbles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICK_RETURN_FUMBLES_COLUMN,
    )
    kick_return_fumbles_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICK_RETURN_FUMBLES_LOST_COLUMN,
    )
    kick_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICK_RETURNS_COLUMN,
    )
    kick_return_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICK_RETURN_TOUCHDOWNS_COLUMN,
    )
    kick_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KICK_RETURN_YARDS_COLUMN,
    )
    long_kick_return: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_KICK_RETURN_COLUMN,
    )
    long_punt_return: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_PUNT_RETURN_COLUMN,
    )
    misc_fumble_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MISC_FUMBLE_RETURNS_COLUMN,
    )
    misc_fumble_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MISC_FUMBLE_RETURN_YARDS_COLUMN,
    )
    opposition_fumble_recoveries: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OPPOSITION_FUMBLE_RECOVERIES_COLUMN,
    )
    opposition_fumble_recovery_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OPPOSITION_FUMBLE_RECOVERY_YARDS_COLUMN,
    )
    opposition_special_team_fumble_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OPPOSITION_SPECIAL_TEAM_FUMBLE_RETURNS_COLUMN,
    )
    opposition_special_team_fumble_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OPPOSITION_SPECIAL_TEAM_FUMBLE_RETURN_YARDS_COLUMN,
    )
    punt_return_fair_catches: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURN_FAIR_CATCHES_COLUMN,
    )
    punt_return_fair_catch_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURN_FAIR_CATCH_PERCENTAGE_COLUMN,
    )
    punt_return_fumbles: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURN_FUMBLES_COLUMN,
    )
    punt_return_fumbles_lost: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURN_FUMBLES_LOST_COLUMN,
    )
    punt_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURNS_COLUMN,
    )
    punt_returns_started_inside_the_10: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURNS_STARTED_INSIDE_THE_10_COLUMN,
    )
    punt_returns_started_inside_the_20: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURNS_STARTED_INSIDE_THE_20_COLUMN,
    )
    punt_return_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURN_TOUCHDOWNS_COLUMN,
    )
    punt_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_RETURN_YARDS_COLUMN,
    )
    special_team_fumble_returns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SPECIAL_TEAM_FUMBLE_RETURNS_COLUMN,
    )
    yards_per_kick_return: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_PER_KICK_RETURN_COLUMN,
    )
    yards_per_punt_return: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_PER_PUNT_RETURN_COLUMN,
    )
    yards_per_return: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YARDS_PER_RETURN_COLUMN,
    )
    average_punt_return_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_PUNT_RETURN_YARDS_COLUMN,
    )
    gross_average_punt_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GROSS_AVERAGE_PUNT_YARDS_COLUMN,
    )
    long_punt: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LONG_PUNT_COLUMN,
    )
    net_average_punt_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_NET_AVERAGE_PUNT_YARDS_COLUMN,
    )
    punts: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_COLUMN,
    )
    punts_blocked: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_BLOCKED_COLUMN,
    )
    punts_blocked_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_BLOCKED_PERCENTAGE_COLUMN,
    )
    punts_inside_10: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_INSIDE_10_COLUMN,
    )
    punts_inside_10_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_INSIDE_10_PERCENTAGE_COLUMN,
    )
    punts_inside_20: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_INSIDE_20_COLUMN,
    )
    punts_inside_20_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_INSIDE_20_PERCENTAGE_COLUMN,
    )
    punts_over_50: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNTS_OVER_50_COLUMN,
    )
    punt_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUNT_YARDS_COLUMN,
    )
    defensive_points: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_POINTS_COLUMN,
    )
    misc_points: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MISC_POINTS_COLUMN,
    )
    return_touchdowns: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RETURN_TOUCHDOWNS_COLUMN,
    )
    total_two_point_conversions: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_TWO_POINT_CONVERSIONS_COLUMN,
    )
    passing_touchdowns_9_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWNS_9_YARDS_COLUMN,
    )
    passing_touchdowns_19_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWNS_19_YARDS_COLUMN,
    )
    passing_touchdowns_29_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWNS_29_YARDS_COLUMN,
    )
    passing_touchdowns_39_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWNS_39_YARDS_COLUMN,
    )
    passing_touchdowns_49_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWNS_49_YARDS_COLUMN,
    )
    passing_touchdowns_above_50_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSING_TOUCHDOWNS_ABOVE_50_YARDS_COLUMN,
    )
    receiving_touchdowns_9_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TOUCHDOWNS_9_YARDS_COLUMN,
    )
    receiving_touchdowns_19_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TOUCHDOWNS_19_YARDS_COLUMN,
    )
    receiving_touchdowns_29_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TOUCHDOWNS_29_YARDS_COLUMN,
    )
    receiving_touchdowns_39_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TOUCHDOWNS_39_YARDS_COLUMN,
    )
    receiving_touchdowns_49_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TOUCHDOWNS_49_YARDS_COLUMN,
    )
    receiving_touchdowns_above_50_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RECEIVING_TOUCHDOWNS_ABOVE_50_YARDS_COLUMN,
    )
    rushing_touchdowns_9_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_TOUCHDOWNS_9_YARDS_COLUMN,
    )
    rushing_touchdowns_19_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_TOUCHDOWNS_19_YARDS_COLUMN,
    )
    rushing_touchdowns_29_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_TOUCHDOWNS_29_YARDS_COLUMN,
    )
    rushing_touchdowns_39_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_TOUCHDOWNS_39_YARDS_COLUMN,
    )
    rushing_touchdowns_49_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_TOUCHDOWNS_49_YARDS_COLUMN,
    )
    rushing_touchdowns_above_50_yards: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUSHING_TOUCHDOWNS_ABOVE_50_YARDS_COLUMN,
    )
    penalties_in_minutes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PENALTIES_IN_MINUTES_COLUMN,
    )
    even_strength_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EVEN_STRENGTH_GOALS_COLUMN,
    )
    power_play_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_POWER_PLAY_GOALS_COLUMN,
    )
    short_handed_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHORT_HANDED_GOALS_COLUMN,
    )
    game_winning_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GAME_WINNING_GOALS_COLUMN,
    )
    even_strength_assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EVEN_STRENGTH_ASSISTS_COLUMN,
    )
    power_play_assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_POWER_PLAY_ASSISTS_COLUMN,
    )
    short_handed_assists: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHORT_HANDED_ASSISTS_COLUMN,
    )
    shots_on_goal: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOTS_ON_GOAL_COLUMN,
    )
    shooting_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOOTING_PERCENTAGE_COLUMN,
    )
    shifts: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHIFTS_COLUMN,
    )
    time_on_ice: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TIME_ON_ICE_COLUMN,
    )
    decision: str | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DECISION_COLUMN,
    )
    goals_against: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GOALS_AGAINST_COLUMN,
    )
    shots_against: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOTS_AGAINST_COLUMN,
    )
    saves: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SAVES_COLUMN,
    )
    save_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SAVE_PERCENTAGE_COLUMN,
    )
    shutouts: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHUTOUTS_COLUMN,
    )
    individual_corsi_for_events: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INDIVIDUAL_CORSI_FOR_EVENTS_COLUMN,
    )
    on_shot_ice_for_events: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ON_SHOT_ICE_FOR_EVENTS_COLUMN,
    )
    on_shot_ice_against_events: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ON_SHOT_ICE_AGAINST_EVENTS_COLUMN,
    )
    corsi_for_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CORSI_FOR_PERCENTAGE_COLUMN,
    )
    relative_corsi_for_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RELATIVE_CORSI_FOR_PERCENTAGE_COLUMN,
    )
    offensive_zone_starts: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OFFENSIVE_ZONE_STARTS_COLUMN,
    )
    defensive_zone_starts: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_ZONE_STARTS_COLUMN,
    )
    offensive_zone_start_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OFFENSIVE_ZONE_START_PERCENTAGE_COLUMN,
    )
    hits: int | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD}, alias=PLAYER_HITS_COLUMN
    )
    true_shooting_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TRUE_SHOOTING_PERCENTAGE_COLUMN,
    )
    at_bats: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AT_BATS_COLUMN,
    )
    runs_scored: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUNS_SCORED_COLUMN,
    )
    runs_batted_in: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RUNS_BATTED_IN_COLUMN,
    )
    bases_on_balls: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BASES_ON_BALLS_COLUMN,
    )
    strikeouts: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STRIKEOUTS_COLUMN,
    )
    plate_appearances: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PLATE_APPEARANCES_COLUMN,
    )
    hits_at_bats: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_HITS_AT_BATS_COLUMN,
    )
    obp: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OBP_COLUMN,
    )
    slg: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SLG_COLUMN,
    )
    ops: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OPS_COLUMN,
    )
    pitches: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PITCHES_COLUMN,
    )
    strikes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STRIKES_COLUMN,
    )
    win_probability_added: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_WIN_PROBABILITY_ADDED_COLUMN,
    )
    average_leverage_index: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_LEVERAGE_INDEX_COLUMN,
    )
    wpa_plus: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_WPA_PLUS_COLUMN,
    )
    wpa_minus: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_WPA_MINUS_COLUMN,
    )
    cwpa: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CWPA_COLUMN,
    )
    acli: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ACLI_COLUMN,
    )
    re24: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RE24_COLUMN,
    )
    putouts: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PUTOUTS_COLUMN,
    )
    innings_pitched: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INNINGS_PITCHED_COLUMN,
    )
    earned_runs: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EARNED_RUNS_COLUMN,
    )
    home_runs: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_HOME_RUNS_COLUMN,
    )
    era: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ERA_COLUMN,
    )
    batters_faced: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BATTERS_FACED_COLUMN,
    )
    strikes_by_contact: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STRIKES_BY_CONTACT_COLUMN,
    )
    strikes_swinging: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STRIKES_SWINGING_COLUMN,
    )
    strikes_looking: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STRIKES_LOOKING_COLUMN,
    )
    ground_balls: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GROUND_BALLS_COLUMN,
    )
    fly_balls: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FLY_BALLS_COLUMN,
    )
    line_drives: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LINE_DRIVES_COLUMN,
    )
    inherited_runners: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INHERITED_RUNNERS_COLUMN,
    )
    inherited_scores: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INHERITED_SCORES_COLUMN,
    )
    effective_field_goal_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EFFECTIVE_FIELD_GOAL_PERCENTAGE_COLUMN,
    )
    penalty_kicks_made: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PENALTY_KICKS_MADE_COLUMN,
    )
    penalty_kicks_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PENALTY_KICKS_ATTEMPTED_COLUMN,
    )
    shots_total: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOTS_TOTAL_COLUMN,
    )
    shots_on_target: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOTS_ON_TARGET_COLUMN,
    )
    yellow_cards: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_YELLOW_CARDS_COLUMN,
    )
    red_cards: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_RED_CARDS_COLUMN,
    )
    touches: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHES_COLUMN,
    )
    expected_goals: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXPECTED_GOALS_COLUMN,
    )
    non_penalty_expected_goals: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_NON_PENALTY_EXPECTED_GOALS_COLUMN,
    )
    expected_assisted_goals: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXPECTED_ASSISTED_GOALS_COLUMN,
    )
    shot_creating_actions: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOT_CREATING_ACTIONS_COLUMN,
    )
    goal_creating_actions: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GOAL_CREATING_ACTIONS_COLUMN,
    )
    passes_completed: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_COMPLETED_COLUMN,
    )
    passes_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_ATTEMPTED_COLUMN,
    )
    pass_completion: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASS_COMPLETION_COLUMN,
    )
    progressive_passes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PROGRESSIVE_PASSES_COLUMN,
    )
    carries: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CARRIES_COLUMN,
    )
    progressive_carries: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PROGRESSIVE_CARRIES_COLUMN,
    )
    take_ons_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TAKE_ONS_ATTEMPTED_COLUMN,
    )
    successful_take_ons: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SUCCESSFUL_TAKE_ONS_COLUMN,
    )
    total_passing_distance: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_PASSING_DISTANCE_COLUMN,
    )
    progressive_passing_distance: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PROGRESSIVE_PASSING_DISTANCE_COLUMN,
    )
    passes_completed_short: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_COMPLETED_SHORT_COLUMN,
    )
    passes_attempted_short: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_ATTEMPTED_SHORT_COLUMN,
    )
    pass_completion_short: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASS_COMPLETION_SHORT_COLUMN,
    )
    passes_completed_medium: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_COMPLETED_MEDIUM_COLUMN,
    )
    passes_attempted_medium: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_ATTEMPTED_MEDIUM_COLUMN,
    )
    pass_completion_medium: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASS_COMPLETION_MEDIUM_COLUMN,
    )
    passes_completed_long: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_COMPLETED_LONG_COLUMN,
    )
    passes_attempted_long: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_ATTEMPTED_LONG_COLUMN,
    )
    pass_completion_long: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASS_COMPLETION_LONG_COLUMN,
    )
    expected_assists: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_EXPECTED_ASSISTS_COLUMN,
    )
    key_passes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_KEY_PASSES_COLUMN,
    )
    passes_into_final_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_INTO_FINAL_THIRD_COLUMN,
    )
    passes_into_penalty_area: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_INTO_PENALTY_AREA_COLUMN,
    )
    crosses_into_penalty_area: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CROSSES_INTO_PENALTY_AREA_COLUMN,
    )
    live_ball_passes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LIVE_BALL_PASSES_COLUMN,
    )
    dead_ball_passes: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEAD_BALL_PASSES_COLUMN,
    )
    passes_from_free_kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_FROM_FREE_KICKS_COLUMN,
    )
    through_balls: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_THROUGH_BALLS_COLUMN,
    )
    switches: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SWITCHES_COLUNM,
    )
    crosses: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CROSSES_COLUMN,
    )
    throw_ins_taken: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_THROW_INS_TAKEN_COLUMN,
    )
    corner_kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CORNER_KICKS_COLUMN,
    )
    inswinging_corner_kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_INSWINGING_CORNER_KICKS_COLUMN,
    )
    outswinging_corner_kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OUTSWINGING_CORNER_KICKS_COLUMN,
    )
    straight_corner_kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_STRAIGHT_CORNER_KICKS_COLUMN,
    )
    passes_offside: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_OFFSIDE_COLUMN,
    )
    passes_blocked: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_BLOCKED_COLUMN,
    )
    tackles_won: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_WON_COLUMN,
    )
    tackles_in_defensive_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_IN_DEFENSIVE_THIRD_COLUMN,
    )
    tackles_in_middle_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_IN_MIDDLE_THIRD_COLUMN,
    )
    tackles_in_attacking_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_IN_ATTACKING_THIRD_COLUMN,
    )
    dribblers_tackled: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DRIBBLERS_TACKLED_COLUMN,
    )
    dribbles_challenged: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DRIBBLES_CHALLENGED_COLUMN,
    )
    percent_of_dribblers_tackled: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERCENT_OF_DRIBBLERS_TACKLED_COLUMN,
    )
    challenges_lost: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CHALLENGES_LOST_COLUMN,
    )
    shots_blocked: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOTS_BLOCKED_COLUMN,
    )
    tackles_plus_interceptions: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLES_PLUS_INTERCEPTIONS_COLUMN,
    )
    errors: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_ERRORS_COLUMN,
    )
    touches_in_defensive_penalty_area: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHES_IN_DEFENSIVE_PENALTY_AREA_COLUMN,
    )
    touches_in_defensive_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHES_IN_DEFENSIVE_THIRD_COLUMN,
    )
    touches_in_middle_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHES_IN_MIDDLE_THIRD_COLUMN,
    )
    touches_in_attacking_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHES_IN_ATTACKING_THIRD_COLUMN,
    )
    touches_in_attacking_penalty_area: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOUCHES_IN_ATTACKING_PENALTY_AREA_COLUMN,
    )
    live_ball_touches: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_LIVE_BALL_TOUCHES_COLUMN,
    )
    successful_take_on_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SUCCESSFUL_TAKE_ON_PERCENTAGE_COLUMN,
    )
    times_tackled_during_take_ons: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TIMES_TACKLED_DURING_TAKE_ONS_COLUMN,
    )
    tackled_during_take_on_percentage: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TACKLED_DURING_TAKE_ON_PERCENTAGE_COLUMN,
    )
    total_carrying_distance: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_TOTAL_CARRYING_DISTANCE_COLUMN,
    )
    progressive_carrying_distance: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PROGRESSIVE_CARRYING_DISTANCE_COLUMN,
    )
    carries_into_final_third: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CARRIES_INTO_FINAL_THIRD_COLUMN,
    )
    carries_into_penalty_area: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CARRIES_INTO_PENALTY_AREA_COLUMN,
    )
    miscontrols: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_MISCONTROLS_COLUMN,
    )
    dispossessed: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DISPOSSESSED_COLUMN,
    )
    passes_received: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_RECEIVED_COLUMN,
    )
    progressive_passes_received: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PROGRESSIVE_PASSES_RECEIVED_COLUMN,
    )
    second_yellow_card: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SECOND_YELLOW_CARD_COLUMN,
    )
    fouls_committed: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FOULS_COMMITTED_COLUMN,
    )
    fouls_drawn: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_FOULS_DRAWN_COLUMN,
    )
    offsides: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OFFSIDES_COLUMN,
    )
    penalty_kicks_won: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PENALTY_KICKS_WON_COLUMN,
    )
    penalty_kicks_conceded: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PENALTY_KICKS_CONCEDED_COLUMN,
    )
    own_goals: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_OWN_GOALS_COLUMN,
    )
    ball_recoveries: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_BALL_RECOVERIES_COLUMN,
    )
    aerials_won: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AERIALS_WON_COLUMN,
    )
    aerials_lost: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AERIALS_LOST_COLUMN,
    )
    percentage_of_aerials_won: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERCENTAGE_OF_AERIALS_WON_COLUMN,
    )
    shots_on_target_against: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_SHOTS_ON_TARGET_AGAINST_COLUMN,
    )
    post_shot_expected_goals: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_POST_SHOT_EXPECTED_GOALS_COLUMN,
    )
    passes_attempted_minus_goal_kicks: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PASSES_ATTEMPTED_MINUS_GOAL_KICKS_COLUMN,
    )
    throws_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_THROWS_ATTEMPTED_COLUMN,
    )
    percentage_of_passes_that_were_launched: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERCENTAGE_OF_PASSES_THAT_WERE_LAUNCHED_COLUMN,
    )
    average_pass_length: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_PASS_LENGTH_COLUMN,
    )
    goal_kicks_attempted: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_GOAL_KICKS_ATTEMPTED_COLUMN,
    )
    percentage_of_goal_kicks_that_were_launched: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERCENTAGE_OF_GOAL_KICKS_THAT_WERE_LAUNCHED_COLUMN,
    )
    average_goal_kick_length: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_GOAL_KICK_LENGTH_COLUMN,
    )
    crosses_faced: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CROSSES_FACED_COLUMN,
    )
    crosses_stopped: int | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_CROSSES_STOPPED_COLUMN,
    )
    percentage_crosses_stopped: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_PERCENTAGE_CROSSES_STOPPED_COLUMN,
    )
    defensive_actions_outside_penalty_area: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_DEFENSIVE_ACTIONS_OUTSIDE_PENALTY_AREA_COLUMN,
    )
    average_distance_of_defensive_actions: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_AVERAGE_DISTANCE_OF_DEFENSIVE_ACTIONS_COLUMN,
    )
    three_point_attempt_rate: float | None = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.LOOKAHEAD},
        alias=PLAYER_THREE_POINT_ATTEMPT_RATE_COLUMN,
    )
