"""Tests for the NBA NBA player model class."""
import datetime
import unittest

import requests_mock
import requests_cache
from sportsball.data.nba.nba.nba_nba_player_model import create_nba_nba_player_model
import pandas as pd


class TestNBANBAPlayerModel(unittest.TestCase):

    def setUp(self):
        self.session = requests_cache.CachedSession(backend="memory")

    def test_identifier(self):
        dt = datetime.datetime(2010, 10, 10, 10, 10, 00)
        with requests_mock.Mocker() as m:
            m.get("https://stats.nba.com/stats/commonplayerinfo?LeagueID=&PlayerID=a")
            player_model = create_nba_nba_player_model(
                pd.Series(data=[
                    "a",
                ], index=[
                    "PERSON_ID",
                ]),
                pd.DataFrame(index=[], columns=["PERSON_ID"]),
                dt,
                self.session,
            )
            self.assertEqual(player_model.identifier, "a")
