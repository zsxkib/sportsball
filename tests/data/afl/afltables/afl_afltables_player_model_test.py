"""Tests for the afltables player model class."""
import unittest

import requests_cache

from sportsball.data.afl.afltables.afl_afltables_player_model import AFLAFLTablesPlayerModel


class TestAFLAFLTablesPlayerModel(unittest.TestCase):

    def setUp(self):
        self._url = "https://afltables.com/afl/stats/players/J/Joel_Amartey.html"
        self._session = requests_cache.CachedSession(backend="memory")
        self._model = AFLAFLTablesPlayerModel(
            self._session,
            self._url,
            "36",
            3,
        )

    def test_kicks(self):
        self.assertEqual(self._model.kicks, 3)
