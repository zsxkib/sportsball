"""Tests for the skill feature class."""
import datetime
import unittest

import sportsball as spb
import pandas as pd
from sportsball.strategy.features.columns import team_identifier_column, team_points_column, player_identifier_column


class TestSkillFeatureClass(unittest.TestCase):

    def setUp(self):
        self._skill_feature = spb.strategy.features.skill_feature.SkillFeature(year_slices=[1])

    def test_process(self):
        df = pd.DataFrame(data={
            spb.data.game_model.FULL_GAME_DT_COLUMN: [datetime.datetime(2009, 12, 31, 0, 0, 0), datetime.datetime(2010, 1, 1, 0, 0, 0)],
            team_identifier_column(0): ["1", "1"],
            team_identifier_column(1): ["2", "2"],
            team_points_column(0): [0, 1],
            team_points_column(1): [2, 3],
            player_identifier_column(0, 0): ["1", "1"],
            player_identifier_column(1, 0): ["2", "2"],
        })
        df = self._skill_feature.process(df)
        self.assertIsNotNone(df)
