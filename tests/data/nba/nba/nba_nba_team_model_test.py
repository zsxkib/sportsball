"""Tests for the NBA NBA team model class."""
import datetime
import unittest

import requests_mock
import requests_cache
from sportsball.data.nba.nba.nba_nba_team_model import create_nba_nba_team_model
from sportsball.data.league import League
import pandas as pd


class TestNBANBATeamModel(unittest.TestCase):

    def setUp(self):
        self.session = requests_cache.CachedSession(backend="memory")

    def test_identifier(self):
        identifier = "a"
        with requests_mock.Mocker() as m:
            m.get("https://news.google.com/rss/search?q=%22my+team+name%22+%2B+%28sport+OR+nba+OR+%22National+Basketball+League%22%29+after%3A2010-10-08+before%3A2010-10-09&ceid=US:en&hl=en&gl=US")
            team_model = create_nba_nba_team_model(
                pd.Series(data=[
                    identifier,
                    "my team name",
                    0.5,
                    70.0,
                ], index=[
                    "TEAM_ID_B",
                    "TEAM_NAME_B",
                    "PTS_B",
                    "FG_B",
                ]),
                False,
                self.session,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NBA,
            )
            self.assertEqual(team_model.identifier, identifier)
