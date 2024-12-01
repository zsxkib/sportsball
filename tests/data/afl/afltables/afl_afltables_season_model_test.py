"""Tests for the afltables season model class."""
import os
import unittest

import requests_cache
import requests_mock

from sportsball.data.afl.afltables.afl_afltables_season_model import AFLAFLTablesSeasonModel
from sportsball.data.season_type import SeasonType


class TestAFLAFLTablesSeasonModel(unittest.TestCase):

    def setUp(self):
        self._url = "https://afltables.com/afl/seas/1897.html"
        self._session = requests_cache.CachedSession(backend="memory")
        self._model = AFLAFLTablesSeasonModel(
            self._session,
            self._url,
            SeasonType.REGULAR,
        )

    def test_ladder(self):
        with requests_mock.Mocker() as m:
            with open(os.path.join(os.path.dirname(__file__), "season_model_test.html")) as handle:
                m.get(self._url, text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "1897_game_0.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/030618970508.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "041518970508.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/041518970508.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "050918970508.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/050918970508.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "111618970508.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/111618970508.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "031618970515.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/031618970515.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "040518970515.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/040518970515.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "061518970515.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/061518970515.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "091118970515.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/091118970515.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "040918970522.html")) as handle:
                m.get("https://afltables.com/afl/stats/games/1897/040918970522.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "melbourne_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/melbourne_idx.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "geelong_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/geelong_idx.html", text=handle.read())
            for count, game in enumerate(self._model.games):
                if count == 7:
                    teams = list(game.teams)
                    self.assertEqual(teams[0].ladder_rank, 4)
                    self.assertEqual(teams[1].ladder_rank, 6)
                    break
