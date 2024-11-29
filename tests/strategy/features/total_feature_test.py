"""Tests for the total feature class."""
import unittest

import pandas as pd
from sportsball.strategy.features.columns import team_identifier_column, player_identifier_column, player_column_prefix
from sportsball.strategy.features.total_feature import TotalFeature, TOTAL_COLUMN_PREFIX, TOTAL_GAMES_COLUMN
from sportsball.data.columns import COLUMN_SEPARATOR


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
        })
        df = self._total_feature.process(df)
        total_games = df[COLUMN_SEPARATOR.join([TOTAL_COLUMN_PREFIX, player_column_prefix(0, 0), TOTAL_GAMES_COLUMN])].values.tolist()
        self.assertListEqual(total_games, [0, 1])
