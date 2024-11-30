"""Tests for the skill feature class."""
import datetime
import unittest

import sportsball as spb
import pandas as pd
from sportsball.strategy.features.columns import team_identifier_column, team_points_column, player_identifier_column, player_column_prefix
from sportsball.strategy.features.skill_feature import _find_matches, SkillFeature, SKILL_COLUMN_PREFIX, SKILL_PROBABILITY_COLUMN
from sportsball.data.columns import COLUMN_SEPARATOR
from openskill.models import PlackettLuce


class TestSkillFeatureClass(unittest.TestCase):

    def setUp(self):
        self._skill_feature = SkillFeature(year_slices=[1])

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
        # df.to_csv("test_tmp.csv")
        self.assertIsNotNone(df)
        print(df.columns.values)
        print(df)
        probability = df[COLUMN_SEPARATOR.join([player_column_prefix(0, None), SKILL_COLUMN_PREFIX, "1", SKILL_PROBABILITY_COLUMN])].values.tolist()
        self.assertListEqual(probability, [0.0, 0.34070897206214457])


    def test_find_matches(self):
        df = pd.DataFrame(data={
            spb.data.game_model.FULL_GAME_DT_COLUMN: [datetime.datetime(2009, 12, 31, 0, 0, 0), datetime.datetime(2010, 1, 1, 0, 0, 0)],
            team_identifier_column(0): ["1", "1"],
            team_identifier_column(1): ["2", "2"],
            team_points_column(0): [0, 1],
            team_points_column(1): [2, 3],
            player_identifier_column(0, 0): ["1", "1"],
            player_identifier_column(1, 0): ["2", "2"],
        })
        team_model = PlackettLuce()
        player_model = PlackettLuce()
        teams = {
            "1": team_model.rating(name="1"),
        }
        players = {
            "1": player_model.rating(name="1"),
        }
        for _, row in df.iterrows():
            _find_matches(row, 1, 5, teams, players)
