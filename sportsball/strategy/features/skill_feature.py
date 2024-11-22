"""The skill feature extractor."""

import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from openskill.models import PlackettLuce, PlackettLuceRating

from ...data.columns import COLUMN_SEPARATOR
from ...data.game_model import FULL_GAME_DT_COLUMN, GAME_COLUMN_SUFFIX
from ...data.player_model import PLAYER_COLUMN_SUFFIX, PLAYER_IDENTIFIER_COLUMN
from ...data.team_model import (POINTS_COLUMN, TEAM_COLUMN_SUFFIX,
                                TEAM_IDENTIFIER_COLUMN)
from .feature import Feature

SKILL_COLUMN_PREFIX = "skill"
SKILL_MU_COLUMN = "mu"
SKILL_SIGMA_COLUMN = "sigma"
SKILL_RANKING_COLUMN = "ranking"
SKILL_PROBABILITY_COLUMN = "probability"


def _find_team_count(df: pd.DataFrame) -> int:
    team_count = 0
    while True:
        team_col = COLUMN_SEPARATOR.join(
            [
                GAME_COLUMN_SUFFIX,
                str(team_count),
                TEAM_COLUMN_SUFFIX,
                TEAM_IDENTIFIER_COLUMN,
            ]
        )
        if team_col not in df.columns.values:
            break
        team_count += 1
    return team_count


def _find_player_count(df: pd.DataFrame, team_count: int) -> int:
    player_count = 0
    while True:
        found_player = False
        for i in range(team_count):
            player_col = COLUMN_SEPARATOR.join(
                [
                    GAME_COLUMN_SUFFIX,
                    str(i),
                    TEAM_COLUMN_SUFFIX,
                    str(player_count),
                    PLAYER_COLUMN_SUFFIX,
                    PLAYER_IDENTIFIER_COLUMN,
                ]
            )
            if player_col not in df.columns.values:
                continue
            found_player = True
        if not found_player:
            break
        player_count += 1
    return player_count


def _slice_df(
    df: pd.DataFrame, date: datetime.date, year_slice: int | None
) -> pd.DataFrame:
    df_slice = df[df[FULL_GAME_DT_COLUMN] < date]
    if year_slice is not None:
        start_date = date - relativedelta(years=year_slice)
        df_slice = df_slice[df_slice[FULL_GAME_DT_COLUMN] > start_date]
    return df_slice


def _create_teams(
    df_slice: pd.DataFrame, team_count: int
) -> tuple[PlackettLuce, dict[str, PlackettLuceRating]]:
    team_model = PlackettLuce()
    teams = {}
    for i in range(team_count):
        team_col = COLUMN_SEPARATOR.join(
            [
                GAME_COLUMN_SUFFIX,
                str(i),
                TEAM_COLUMN_SUFFIX,
                TEAM_IDENTIFIER_COLUMN,
            ]
        )
        for team_identifier in df_slice[team_col].unique():
            if team_identifier in teams:
                continue
            teams[team_identifier] = team_model.rating(name=team_identifier)
    return team_model, teams


def _create_player_teams(
    df_slice: pd.DataFrame, team_count: int, player_count: int
) -> tuple[PlackettLuce, dict[str, PlackettLuceRating]]:
    player_model = PlackettLuce()
    players = {}
    for i in range(player_count):
        for i in range(team_count):
            player_col = COLUMN_SEPARATOR.join(
                [
                    GAME_COLUMN_SUFFIX,
                    str(i),
                    TEAM_COLUMN_SUFFIX,
                    str(player_count),
                    PLAYER_COLUMN_SUFFIX,
                    PLAYER_IDENTIFIER_COLUMN,
                ]
            )
            if player_col not in df_slice.columns.values:
                continue
            for player_identifier in df_slice[player_col].unique():
                players[player_identifier] = player_model.rating(name=player_identifier)
    return player_model, players


def _find_matches(
    row: pd.Series,
    team_count: int,
    player_count: int,
    teams: dict[str, PlackettLuceRating],
    players: dict[str, PlackettLuceRating],
) -> tuple[list[float], list[list[PlackettLuceRating]], list[list[PlackettLuceRating]]]:
    points = []
    team_match = []
    player_match = []
    for i in range(team_count):
        points_col = COLUMN_SEPARATOR.join(
            [
                GAME_COLUMN_SUFFIX,
                str(i),
                TEAM_COLUMN_SUFFIX,
                POINTS_COLUMN,
            ]
        )
        if row[points_col].isnull():
            continue
        points.append(float(row[points_col]))
        team_col = COLUMN_SEPARATOR.join(
            [
                GAME_COLUMN_SUFFIX,
                str(i),
                TEAM_COLUMN_SUFFIX,
                TEAM_IDENTIFIER_COLUMN,
            ]
        )
        team_idx = row[team_col]
        team_match.append([teams[team_idx]])
        player_team = []
        for j in range(player_count):
            player_col = COLUMN_SEPARATOR.join(
                [
                    GAME_COLUMN_SUFFIX,
                    str(i),
                    TEAM_COLUMN_SUFFIX,
                    str(j),
                    PLAYER_COLUMN_SUFFIX,
                    PLAYER_IDENTIFIER_COLUMN,
                ]
            )
            if row[player_col].isnull():
                continue
            player_team.append(players[row[player_col]])
        player_match.append(player_team)
    return points, team_match, player_match


def _rate_match(
    model: PlackettLuce,
    match: list[list[PlackettLuceRating]],
    points: list[float],
    ratings: dict[str, PlackettLuceRating],
) -> dict[str, PlackettLuceRating]:
    output = model.rate(match, scores=points)
    for team in output:
        for player in team:
            name = player.name
            if name is None:
                continue
            ratings[name] = player
    return ratings


def _simulate_games(
    df_slice: pd.DataFrame,
    team_count: int,
    player_count: int,
    model_team: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
    model_players: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
) -> tuple[
    tuple[PlackettLuce, dict[str, PlackettLuceRating]],
    tuple[PlackettLuce, dict[str, PlackettLuceRating]],
]:
    team_model, teams = model_team
    player_model, players = model_players
    for _, row in df_slice.iterrows():
        points, team_match, player_match = _find_matches(
            row, team_count, player_count, teams, players
        )
        teams = _rate_match(team_model, team_match, points, teams)
        players = _rate_match(player_model, player_match, points, players)
    return (team_model, teams), (player_model, players)


def _find_player_team(
    player_count: int,
    players: dict[str, PlackettLuceRating],
    row: pd.Series,
    year_col: str,
    team_index: int,
) -> list[PlackettLuceRating]:
    player_team = []
    for j in range(player_count):
        player_col_prefix = COLUMN_SEPARATOR.join(
            [
                GAME_COLUMN_SUFFIX,
                str(team_index),
                TEAM_COLUMN_SUFFIX,
                str(j),
                PLAYER_COLUMN_SUFFIX,
            ]
        )
        player_idx_col = COLUMN_SEPARATOR.join(
            [player_col_prefix, PLAYER_IDENTIFIER_COLUMN]
        )
        if row[player_idx_col].isnull():
            continue
        player_idx = row[player_idx_col]
        player_skill_col_prefix = COLUMN_SEPARATOR.join(
            [player_col_prefix, SKILL_COLUMN_PREFIX, year_col]
        )
        player_mu_col = COLUMN_SEPARATOR.join(
            [player_skill_col_prefix, SKILL_MU_COLUMN]
        )
        player_sigma_col = COLUMN_SEPARATOR.join(
            [player_skill_col_prefix, SKILL_SIGMA_COLUMN]
        )
        player = players[player_idx]
        row[player_mu_col] = player.mu
        row[player_sigma_col] = player.sigma
        player_team.append(player)
    return player_team


def _find_team_team(
    team_index: int, row: pd.Series, year_col: str, teams: dict[str, PlackettLuceRating]
) -> tuple[list[PlackettLuceRating], pd.Series]:
    team_col_prefix = COLUMN_SEPARATOR.join(
        [GAME_COLUMN_SUFFIX, str(team_index), TEAM_COLUMN_SUFFIX]
    )
    team_idx_col = COLUMN_SEPARATOR.join([team_col_prefix, TEAM_IDENTIFIER_COLUMN])
    if row[team_idx_col].isnull():
        return [], row
    team_idx = row[team_idx_col]
    team_skill_col_prefix = COLUMN_SEPARATOR.join(
        [team_col_prefix, SKILL_COLUMN_PREFIX, year_col]
    )
    team_mu_col = COLUMN_SEPARATOR.join([team_skill_col_prefix, SKILL_MU_COLUMN])
    team_sigma_col = COLUMN_SEPARATOR.join([team_skill_col_prefix, SKILL_SIGMA_COLUMN])
    team = teams[team_idx]
    row[team_mu_col] = team.mu
    row[team_sigma_col] = team.sigma
    return [team], row


def _find_row_matches(
    row: pd.Series,
    counts: tuple[int, int],
    year_col: str,
    teams: dict[str, PlackettLuceRating],
    players: dict[str, PlackettLuceRating],
) -> tuple[pd.Series, list[list[PlackettLuceRating]], list[list[PlackettLuceRating]]]:
    team_count, player_count = counts
    team_match = []
    player_match = []
    for i in range(team_count):
        team, row = _find_team_team(i, row, year_col, teams)
        if not team:
            continue
        team_match.append(team)
        player_team = _find_player_team(player_count, players, row, year_col, i)
        player_match.append(player_team)
    return row, team_match, player_match


def _rank_team_predictions(
    team_match: list[list[PlackettLuceRating]],
    row: pd.Series,
    team_model: PlackettLuce,
    year_col: str,
) -> pd.Series:
    rank_team_predictions = team_model.predict_rank(team_match)
    for i, (rank, prob) in enumerate(rank_team_predictions):
        team_skill_col_prefix = COLUMN_SEPARATOR.join(
            [
                GAME_COLUMN_SUFFIX,
                str(i),
                TEAM_COLUMN_SUFFIX,
                SKILL_COLUMN_PREFIX,
                year_col,
            ]
        )
        team_ranking_col = COLUMN_SEPARATOR.join(
            [team_skill_col_prefix, SKILL_RANKING_COLUMN]
        )
        team_prob_col = COLUMN_SEPARATOR.join(
            [team_skill_col_prefix, SKILL_PROBABILITY_COLUMN]
        )
        row[team_ranking_col] = rank
        row[team_prob_col] = prob
    return row


def _rank_player_predictions(
    row: pd.Series,
    player_model: PlackettLuce,
    player_match: list[list[PlackettLuceRating]],
    year_col: str,
) -> pd.Series:
    rank_player_predictions = player_model.predict_rank(player_match)
    for i, (rank, prob) in enumerate(rank_player_predictions):
        for j in range(len(player_match[i])):
            player_skill_col_prefix = COLUMN_SEPARATOR.join(
                [
                    GAME_COLUMN_SUFFIX,
                    str(i),
                    TEAM_COLUMN_SUFFIX,
                    str(j),
                    PLAYER_COLUMN_SUFFIX,
                    SKILL_COLUMN_PREFIX,
                    year_col,
                ]
            )
            player_ranking_col = COLUMN_SEPARATOR.join(
                [player_skill_col_prefix, SKILL_RANKING_COLUMN]
            )
            player_prob_col = COLUMN_SEPARATOR.join(
                [player_skill_col_prefix, SKILL_PROBABILITY_COLUMN]
            )
            row[player_ranking_col] = rank
            row[player_prob_col] = prob
    return row


def _create_feature_cols(
    group: pd.DataFrame,
    year_slice: int | None,
    counts: tuple[int, int],
    model_team: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
    model_players: tuple[PlackettLuce, dict[str, PlackettLuceRating]],
) -> pd.DataFrame:
    year_col = str(year_slice) if year_slice is not None else "all"
    team_model, teams = model_team
    player_model, players = model_players
    for _, row in group.iterrows():
        row, team_match, player_match = _find_row_matches(
            row, counts, year_col, teams, players
        )
        row = _rank_team_predictions(team_match, row, team_model, year_col)
        row = _rank_player_predictions(row, player_model, player_match, year_col)
    return group


class SkillFeature(Feature):
    """The skill feature extractor class."""

    # pylint: disable=too-few-public-methods

    def __init__(self, year_slices: list[int | None]) -> None:
        super().__init__()
        self._year_slices = year_slices

    def _create_columns(
        self, df: pd.DataFrame, team_count: int, player_count: int
    ) -> pd.DataFrame:
        for year_slice in self._year_slices:
            year_col = str(year_slice) if year_slice is not None else "all"
            for i in range(team_count):
                for team_col_suffix in [
                    SKILL_MU_COLUMN,
                    SKILL_SIGMA_COLUMN,
                    SKILL_RANKING_COLUMN,
                    SKILL_PROBABILITY_COLUMN,
                ]:
                    team_col = COLUMN_SEPARATOR.join(
                        [
                            GAME_COLUMN_SUFFIX,
                            str(i),
                            TEAM_COLUMN_SUFFIX,
                            SKILL_COLUMN_PREFIX,
                            year_col,
                            team_col_suffix,
                        ]
                    )
                    df[team_col] = 0.0
                for j in range(player_count):
                    for player_col_suffix in [
                        SKILL_MU_COLUMN,
                        SKILL_SIGMA_COLUMN,
                        SKILL_RANKING_COLUMN,
                        SKILL_PROBABILITY_COLUMN,
                    ]:
                        player_col = COLUMN_SEPARATOR.join(
                            [
                                GAME_COLUMN_SUFFIX,
                                str(i),
                                TEAM_COLUMN_SUFFIX,
                                str(j),
                                PLAYER_COLUMN_SUFFIX,
                                SKILL_COLUMN_PREFIX,
                                year_col,
                                player_col_suffix,
                            ]
                        )
                        df[player_col] = 0.0
        return df

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the dataframe and add the necessary features."""
        team_count = _find_team_count(df)
        player_count = _find_player_count(df, team_count)
        self._create_columns(df, team_count, player_count)

        for date, group in df.groupby([df[FULL_GAME_DT_COLUMN].dt.date]):
            for year_slice in self._year_slices:
                df_slice = _slice_df(df, date, year_slice)  # type: ignore
                team_model, teams = _create_teams(df_slice, team_count)
                player_model, players = _create_player_teams(
                    df_slice, team_count, player_count
                )
                (team_model, teams), (player_model, players) = _simulate_games(
                    df_slice,
                    team_count,
                    player_count,
                    (team_model, teams),
                    (player_model, players),
                )
                group = _create_feature_cols(
                    group,
                    year_slice,
                    (team_count, player_count),
                    (team_model, teams),
                    (player_model, players),
                )

        return df
