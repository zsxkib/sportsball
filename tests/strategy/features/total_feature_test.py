"""Tests for the total feature class."""
import unittest

import pandas as pd
from sportsball.strategy.features.columns import \
    team_identifier_column, player_identifier_column, player_column_prefix, venue_identifier_column, team_column_prefix, kick_column
from sportsball.strategy.features.total_feature import TotalFeature, TOTAL_COLUMN_PREFIX, TOTAL_GAMES_COLUMN, TOTAL_KICKS_COLUMN
from sportsball.data.game_model import VENUE_COLUMN_PREFIX
from sportsball.data.league_model import DELIMITER


class TestTotalFeature(unittest.TestCase):

    def setUp(self):
        self._total_feature = TotalFeature()

    def test_process(self):
        df = pd.DataFrame(data={
            team_identifier_column(0): ["1", "1"],
            team_identifier_column(1): ["2", "2"],
            player_identifier_column(0, 0): ["p1", "p1"],
            player_identifier_column(0, 1): ["p2", "p2"],
            player_identifier_column(1, 0): ["p3", "p3"],
            player_identifier_column(1, 1): ["p4", "p4"],
            kick_column(0, 0): [0, 1],
            kick_column(0, 1): [1, 2],
            kick_column(1, 0): [3, 4],
            kick_column(1, 1): [5, 6],
        })
        df = self._total_feature.process(df)
        total_games = df[DELIMITER.join([TOTAL_COLUMN_PREFIX, player_column_prefix(0, 0), TOTAL_GAMES_COLUMN])].values.tolist()
        self.assertListEqual(total_games, [0, 1])
        total_team_kicks = df[DELIMITER.join([TOTAL_COLUMN_PREFIX, team_column_prefix(0), TOTAL_KICKS_COLUMN])].values.tolist()
        self.assertListEqual(total_team_kicks, [1, 3])

    def test_team_venue_total_games(self):
        df = pd.DataFrame(data={
            team_identifier_column(0): ["t1", "t1", "t1"],
            team_identifier_column(1): ["t2", "t2", "t2"],
            venue_identifier_column(): ["v1", "v1", "v1"],
            kick_column(0, 0): [0, 1, 2],
            kick_column(0, 1): [1, 2, 3],
            kick_column(1, 0): [3, 4, 5],
            kick_column(1, 1): [5, 6, 7],
        })
        df = self._total_feature.process(df)
        total_games = df[DELIMITER.join([TOTAL_COLUMN_PREFIX, team_column_prefix(0), VENUE_COLUMN_PREFIX, TOTAL_GAMES_COLUMN])].values.tolist()
        self.assertListEqual(total_games, [0, 1, 2])
