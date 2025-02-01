"""Tests for the afltables league model class."""
import unittest

import requests_cache
from sportsball.data.afl.afltables.afl_afltables_league_model import AFLAFLTablesLeagueModel
from sportsball.data.league import League


class TestAFLTablesLeagueModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self._league_model = AFLAFLTablesLeagueModel(self._session)

    def test_league(self):
        self.assertEqual(self._league_model.league, League.AFL)
