"""Tests for the lag feature class."""
import unittest

import pandas as pd
from sportsball.strategy.features.columns import team_identifier_column, venue_identifier_column, attendance_column
from sportsball.strategy.features.lag_feature import LagFeature, LAG_COLUMN_PREFIX
from sportsball.data.columns import COLUMN_SEPARATOR


class TestLagFeature(unittest.TestCase):

    def setUp(self):
        self._lag_feature = LagFeature()

    def test_process(self):
        df = pd.DataFrame(data={
            team_identifier_column(0): ["1", "1"],
            team_identifier_column(1): ["2", "2"],
            venue_identifier_column(): ["4", "4"],
            attendance_column(): [12000, 13000]
        })
        df = self._lag_feature.process(df)
        lag_attendances = df[COLUMN_SEPARATOR.join([LAG_COLUMN_PREFIX, attendance_column()])].values.tolist()
        self.assertListEqual(lag_attendances, [None, 12000])
